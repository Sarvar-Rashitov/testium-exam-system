from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Avg, Count, Max, Min
from .models import Result
from exams.models import ExamLink
from students.models import Student
import json
import csv


@csrf_exempt
def submit_exam_view(request):
    """Submit exam (AJAX endpoint)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            student_id = data.get('student_id')
            exam_link_token = data.get('exam_link_token')
            answers = data.get('answers', {})
            time_taken = data.get('time_taken', 0)
            tab_switches = data.get('tab_switches', 0)
            started_at = data.get('started_at')
            
            # Validate
            exam_link = get_object_or_404(ExamLink, unique_token=exam_link_token)
            student = get_object_or_404(Student, pk=student_id)
            exam = exam_link.exam
            
            # Calculate score - TODO: Update for new question structure
            # questions = Question.objects.filter(exam=exam)
            total_points = 100  # Temporary placeholder
            earned_points = 0  # Temporary placeholder
            
            # TODO: Implement scoring for new question structure
            # for question in questions:
            #     if question.type == 'multiple_choice':
            #         student_answer = answers.get(str(question.id), '').strip().upper()
            #         if student_answer == question.correct_answer.strip().upper():
            #             earned_points += question.points
            
            percentage = (earned_points / total_points * 100) if total_points > 0 else 0
            
            # Create result
            result = Result.objects.create(
                student=student,
                exam=exam,
                exam_link=exam_link,
                score=earned_points,
                total_points=total_points,
                percentage=percentage,
                answers=answers,
                time_taken=time_taken,
                tab_switches=tab_switches,
                started_at=timezone.datetime.fromisoformat(started_at.replace('Z', '+00:00'))
            )
            
            return JsonResponse({
                'success': True,
                'result_id': result.id,
                'score': earned_points,
                'total_points': total_points,
                'percentage': round(percentage, 2),
                'band_score': result.band_score
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


def result_view(request, pk):
    """View result (public)"""
    result = get_object_or_404(Result, pk=pk)
    # TODO: Update for new question structure
    # questions = result.exam.questions.all().order_by('order')
    
    # Add correct/incorrect info to questions
    question_results = []
    # TODO: Implement for new question structure
    # for question in questions:
    #     student_answer = result.answers.get(str(question.id), '')
    #     is_correct = False
    #     if question.type == 'multiple_choice':
    #         is_correct = student_answer.strip().upper() == question.correct_answer.strip().upper()
    #     
    #     question_results.append({
    #         'question': question,
    #         'student_answer': student_answer,
    #         'is_correct': is_correct
    #     })
    
    context = {
        'result': result,
        'question_results': question_results,
        'time_taken_minutes': result.time_taken // 60 if result.time_taken else 0
    }
    
    return render(request, 'results/result_detail.html', context)


@login_required
def results_list_view(request):
    """List all results (admin)"""
    results = Result.objects.filter(exam__organization=request.user).select_related('student', 'exam')
    
    # Filter by exam
    exam_id = request.GET.get('exam_id')
    if exam_id:
        results = results.filter(exam_id=exam_id)
    
    context = {
        'results': results,
        'selected_exam_id': exam_id
    }
    
    return render(request, 'results/results_list.html', context)


@login_required
def analytics_view(request):
    """Analytics dashboard"""
    exam_id = request.GET.get('exam_id')
    results = Result.objects.filter(exam__organization=request.user)
    
    if exam_id:
        results = results.filter(exam_id=exam_id)
    
    # Calculate analytics
    analytics = results.aggregate(
        total_students=Count('student', distinct=True),
        total_attempts=Count('id'),
        avg_score=Avg('score'),
        avg_percentage=Avg('percentage'),
        max_score=Max('score'),
        min_score=Min('score'),
        avg_time_taken=Avg('time_taken')
    )
    
    # Score distribution
    score_distribution = [
        {'range': '0-20%', 'count': results.filter(percentage__lt=20).count()},
        {'range': '20-40%', 'count': results.filter(percentage__gte=20, percentage__lt=40).count()},
        {'range': '40-60%', 'count': results.filter(percentage__gte=40, percentage__lt=60).count()},
        {'range': '60-80%', 'count': results.filter(percentage__gte=60, percentage__lt=80).count()},
        {'range': '80-100%', 'count': results.filter(percentage__gte=80).count()},
    ]
    
    # Top students
    top_students = results.order_by('-score')[:10]
    
    # Get exams for filter
    from exams.models import Exam
    exams = Exam.objects.filter(organization=request.user)
    
    context = {
        'analytics': analytics,
        'score_distribution': score_distribution,
        'top_students': top_students,
        'exams': exams,
        'selected_exam_id': exam_id
    }
    
    return render(request, 'results/analytics.html', context)


@login_required
def export_csv_view(request):
    """Export results to CSV"""
    exam_id = request.GET.get('exam_id')
    results = Result.objects.filter(exam__organization=request.user).select_related('student', 'exam')
    
    if exam_id:
        results = results.filter(exam_id=exam_id)
    
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="natijalar.csv"'
    
    # Add BOM for Excel UTF-8 support
    response.write('\ufeff')
    
    writer = csv.writer(response)
    writer.writerow(['Talaba', 'Telefon', 'Telegram', 'Imtihon', 'Ball', 'Foiz', 'IELTS Band', 'Vaqt (daq)', 'Sana'])
    
    for result in results:
        writer.writerow([
            result.student.full_name,
            result.student.phone,
            result.student.telegram_username,
            result.exam.title,
            f"{result.score}/{result.total_points}",
            f"{result.percentage:.1f}%",
            result.band_score,
            result.time_taken // 60 if result.time_taken else 0,
            result.completed_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response
