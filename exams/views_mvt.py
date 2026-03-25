from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Exam, Section, QuestionGroup, ExamLink
from .forms import ExamForm, SectionForm, QuestionGroupForm, ExamLinkForm
from students.forms import StudentRegistrationForm
from students.models import Student


@login_required
def exam_list_view(request):
    """List all exams"""
    exams = Exam.objects.filter(organization=request.user).prefetch_related('sections')
    return render(request, 'exams/exam_list.html', {'exams': exams})


@login_required
def exam_create_view(request):
    """Create new exam"""
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.organization = request.user
            exam.save()
            messages.success(request, 'Imtihon muvaffaqiyatli yaratildi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm()
    
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Yangi imtihon'})


@login_required
def exam_detail_view(request, pk):
    """Exam detail view"""
    exam = get_object_or_404(Exam, pk=pk, organization=request.user)
    sections = exam.sections.all().order_by('order')
    links = exam.links.all()
    
    # Count total questions across all sections
    total_questions = 0
    for section in sections:
        for group in section.question_groups.all():
            # Count questions in each group based on question type
            if group.question_type == 'multiple_choice_single':
                total_questions += group.multiplechoicesinglequestion_set.count()
            elif group.question_type == 'multiple_choice_multiple':
                total_questions += group.multiplechoicemultiplequestion_set.count()
            elif group.question_type == 'true_false_ng':
                total_questions += group.truefalsenotgivenquestion_set.count()
            elif group.question_type == 'yes_no_ng':
                total_questions += group.yesnonotgivenquestion_set.count()
            elif group.question_type == 'sentence_completion':
                total_questions += group.sentencecompletionquestion_set.count()
            elif group.question_type == 'short_answer':
                total_questions += group.shortanswerquestion_set.count()
            elif group.question_type == 'diagram_labeling':
                total_questions += group.diagramlabelingquestion_set.count()
            elif group.question_type == 'summary_completion':
                total_questions += group.summarycompletionquestion_set.count()
    
    context = {
        'exam': exam,
        'sections': sections,
        'links': links,
        'total_questions': total_questions
    }
    
    return render(request, 'exams/exam_detail.html', context)


@login_required
def exam_edit_view(request, pk):
    """Edit exam"""
    exam = get_object_or_404(Exam, pk=pk, organization=request.user)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imtihon yangilandi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamForm(instance=exam)
    
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Imtihonni tahrirlash', 'exam': exam})


@login_required
def exam_delete_view(request, pk):
    """Delete exam"""
    exam = get_object_or_404(Exam, pk=pk, organization=request.user)
    
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Imtihon o\'chirildi!')
        return redirect('exam_list')
    
    return render(request, 'exams/exam_confirm_delete.html', {'exam': exam})


@login_required
def section_create_view(request, exam_pk):
    """Create section for exam"""
    exam = get_object_or_404(Exam, pk=exam_pk, organization=request.user)
    
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)
        if form.is_valid():
            section = form.save(commit=False)
            section.exam = exam
            section.save()
            messages.success(request, 'Section muvaffaqiyatli yaratildi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = SectionForm()
    
    return render(request, 'exams/section_form.html', {
        'form': form,
        'exam': exam,
        'title': 'Yangi Section'
    })


@login_required
def question_group_create_view(request, section_pk):
    """Create question group for section"""
    section = get_object_or_404(Section, pk=section_pk, exam__organization=request.user)
    
    if request.method == 'POST':
        form = QuestionGroupForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.section = section
            group.save()
            messages.success(request, 'Savol guruhi yaratildi!')
            return redirect('question_group_detail', pk=group.pk)
    else:
        form = QuestionGroupForm()
    
    return render(request, 'exams/question_group_form.html', {
        'form': form,
        'section': section,
        'title': 'Yangi savol guruhi'
    })


@login_required
def question_group_detail_view(request, pk):
    """Question group detail - shows all questions in this group"""
    group = get_object_or_404(QuestionGroup, pk=pk, section__exam__organization=request.user)
    
    # Get questions based on type
    questions = []
    if group.question_type == 'multiple_choice_single':
        questions = group.multiplechoicesinglequestion_set.all()
    elif group.question_type == 'multiple_choice_multiple':
        questions = group.multiplechoicemultiplequestion_set.all()
    elif group.question_type == 'true_false_ng':
        questions = group.truefalsenotgivenquestion_set.all()
    elif group.question_type == 'yes_no_ng':
        questions = group.yesnonotgivenquestion_set.all()
    elif group.question_type == 'sentence_completion':
        questions = group.sentencecompletionquestion_set.all()
    elif group.question_type == 'short_answer':
        questions = group.shortanswerquestion_set.all()
    elif group.question_type == 'diagram_labeling':
        questions = group.diagramlabelingquestion_set.all()
    elif group.question_type == 'summary_completion':
        questions = group.summarycompletionquestion_set.all()
    
    context = {
        'group': group,
        'questions': questions,
        'section': group.section,
        'exam': group.section.exam
    }
    
    return render(request, 'exams/question_group_detail.html', context)


@login_required
def question_create_view(request, group_pk):
    """Add question to group - redirects to specific form based on question type"""
    group = get_object_or_404(QuestionGroup, pk=group_pk, section__exam__organization=request.user)
    
    # Redirect to specific question form based on group type
    type_url_map = {
        'multiple_choice_single': 'question_mcq_single_create',
        'multiple_choice_multiple': 'question_mcq_multiple_create',
        'true_false_ng': 'question_tfng_create',
        'yes_no_ng': 'question_ynng_create',
        'sentence_completion': 'question_sentence_create',
        'short_answer': 'question_short_answer_create',
        'diagram_labeling': 'question_diagram_create',
        'summary_completion': 'question_summary_create',
    }
    
    url_name = type_url_map.get(group.question_type)
    if url_name:
        return redirect(url_name, group_pk=group_pk)
    else:
        messages.error(request, 'Bu savol turi uchun forma hali tayyor emas')
        return redirect('question_group_detail', pk=group_pk)


# Placeholder views for specific question types - will be implemented with forms
@login_required
def question_mcq_single_create_view(request, group_pk):
    """Create MCQ single answer question"""
    group = get_object_or_404(QuestionGroup, pk=group_pk)
    messages.info(request, 'MCQ Single forma hali ishlab chiqilmoqda')
    return redirect('question_group_detail', pk=group_pk)


@login_required
def question_delete_view(request, pk):
    """Delete question - placeholder"""
    messages.info(request, 'Savol o\'chirish funksiyasi hali ishlab chiqilmoqda')
    return redirect('exam_list')


@login_required
def generate_link_view(request, exam_pk):
    """Generate exam link"""
    exam = get_object_or_404(Exam, pk=exam_pk, organization=request.user)
    
    if request.method == 'POST':
        form = ExamLinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.exam = exam
            expires_in_days = form.cleaned_data.get('expires_in_days')
            if expires_in_days:
                link.expires_at = timezone.now() + timedelta(days=expires_in_days)
            link.save()
            messages.success(request, 'Link yaratildi!')
            return redirect('exam_detail', pk=exam.pk)
    else:
        form = ExamLinkForm()
    
    return render(request, 'exams/link_form.html', {'form': form, 'exam': exam})


def exam_start_view(request, token):
    """Public exam start view"""
    exam_link = get_object_or_404(ExamLink, unique_token=token)
    
    if not exam_link.is_valid():
        return render(request, 'exams/link_expired.html', {'exam_link': exam_link})
    
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            exam_link.use_count += 1
            exam_link.save()
            return redirect('exam_take', token=token, student_id=student.id)
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'exams/exam_start.html', {
        'form': form,
        'exam': exam_link.exam,
        'exam_link': exam_link
    })


def exam_take_view(request, token, student_id):
    """Exam taking view"""
    exam_link = get_object_or_404(ExamLink, unique_token=token)
    student = get_object_or_404(Student, pk=student_id)
    exam = exam_link.exam
    sections = exam.sections.all().order_by('order')
    
    context = {
        'exam': exam,
        'sections': sections,
        'student': student,
        'exam_link': exam_link,
        'duration_seconds': exam.duration * 60
    }
    
    return render(request, 'exams/exam_take.html', context)
