from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .forms import OrganizationRegistrationForm, OrganizationLoginForm
from .models import Teacher
from exams.models import Exam
from results.models import Result
from django.db.models import Count, Avg, Q


def auth_view(request):
    """Combined authentication view for both login and register"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    login_form = OrganizationLoginForm()
    register_form = OrganizationRegistrationForm()
    
    return render(request, 'organizations/auth.html', {
        'login_form': login_form,
        'register_form': register_form
    })


def register_view(request):
    """Organization registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OrganizationRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Check if "Remember Me" is checked
            remember_me = request.POST.get('remember_me')
            if not remember_me:
                # Session expires when browser closes
                request.session.set_expiry(0)
            else:
                # Session expires after 2 weeks (1209600 seconds)
                request.session.set_expiry(1209600)
            
            # Specify the backend when logging in
            backend = 'organizations.backends.EmailBackend'
            login(request, user, backend=backend)
            messages.success(request, 'Registration successful! Welcome!')
            return redirect('dashboard')
        else:
            # If form has errors, show them on the auth page
            login_form = OrganizationLoginForm()
            return render(request, 'organizations/auth.html', {
                'login_form': login_form,
                'register_form': form
            })
    
    return redirect('auth')


def login_view(request):
    """Organization login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OrganizationLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # username field contains email
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Specify the backend when logging in
                backend = 'organizations.backends.EmailBackend'
                login(request, user, backend=backend)
                messages.success(request, f'Welcome back, {user.full_name}!')
                return redirect('dashboard')
        else:
            # If form has errors, show them on the auth page
            register_form = OrganizationRegistrationForm()
            return render(request, 'organizations/auth.html', {
                'login_form': form,
                'register_form': register_form
            })
    
    return redirect('auth')


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('auth')


@login_required
def dashboard_view(request):
    """Admin dashboard view"""
    exams = Exam.objects.filter(organization=request.user)
    total_exams = exams.count()
    active_exams = exams.filter(is_active=True).count()
    
    results = Result.objects.filter(exam__organization=request.user)
    total_students = results.values('student').distinct().count()
    total_attempts = results.count()
    avg_score = results.aggregate(Avg('percentage'))['percentage__avg'] or 0
    
    # Recent activity - last 7 days
    from datetime import timedelta
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_activity = results.filter(completed_at__gte=seven_days_ago)
    
    # Group by date for chart
    activity_by_date = {}
    for result in recent_activity:
        date_key = result.completed_at.strftime('%Y-%m-%d')
        activity_by_date[date_key] = activity_by_date.get(date_key, 0) + 1
    
    # Sort by date
    activity_data = [{'date': k, 'count': v} for k, v in sorted(activity_by_date.items())]
    
    # Score distribution for quick view
    score_ranges = {
        'low': results.filter(percentage__lt=50).count(),
        'medium': results.filter(percentage__gte=50, percentage__lt=75).count(),
        'high': results.filter(percentage__gte=75).count()
    }
    
    # Limit to 4 items for dashboard
    # Show best results (highest percentage)
    recent_results = results.select_related('student', 'exam').order_by('-percentage', '-completed_at')[:4]
    recent_exams = exams.order_by('-created_at')[:4]
    
    context = {
        'total_exams': total_exams,
        'active_exams': active_exams,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 2),
        'recent_results': recent_results,
        'exams': recent_exams,
        'activity_data': activity_data,
        'score_ranges': score_ranges
    }
    
    return render(request, 'organizations/dashboard.html', context)


@login_required
def teacher_list_view(request):
    """List all teachers"""
    teachers = Teacher.objects.filter(organization=request.user).annotate(
        student_count=Count('students', distinct=True)
    )
    
    context = {
        'teachers': teachers
    }
    
    return render(request, 'organizations/teacher_list.html', context)


@login_required
def teacher_create_view(request):
    """Create new teacher"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        
        Teacher.objects.create(
            organization=request.user,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            subject=subject
        )
        
        messages.success(request, 'O\'qituvchi muvaffaqiyatli qo\'shildi!')
        return redirect('teacher_list')
    
    return render(request, 'organizations/teacher_form.html', {'title': 'Yangi o\'qituvchi'})


@login_required
def teacher_edit_view(request, pk):
    """Edit teacher"""
    teacher = get_object_or_404(Teacher, pk=pk, organization=request.user)
    
    if request.method == 'POST':
        teacher.first_name = request.POST.get('first_name')
        teacher.last_name = request.POST.get('last_name')
        teacher.phone = request.POST.get('phone', '')
        teacher.email = request.POST.get('email', '')
        teacher.subject = request.POST.get('subject', '')
        teacher.is_active = request.POST.get('is_active') == 'on'
        teacher.save()
        
        messages.success(request, 'O\'qituvchi ma\'lumotlari yangilandi!')
        return redirect('teacher_list')
    
    context = {
        'teacher': teacher,
        'title': 'O\'qituvchini tahrirlash'
    }
    
    return render(request, 'organizations/teacher_form.html', context)


@login_required
def teacher_delete_view(request, pk):
    """Delete teacher"""
    teacher = get_object_or_404(Teacher, pk=pk, organization=request.user)
    
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'O\'qituvchi o\'chirildi!')
        return redirect('teacher_list')
    
    context = {
        'teacher': teacher
    }
    
    return render(request, 'organizations/teacher_confirm_delete.html', context)


@login_required
def teacher_statistics_view(request):
    """Teacher statistics view"""
    from django.db.models import Avg, Count
    
    # Get all teachers for selector
    all_teachers = Teacher.objects.filter(
        organization=request.user, 
        is_active=True
    ).annotate(
        student_count=Count('students', distinct=True)
    ).order_by('first_name')
    
    # Get selected teacher or default to first teacher
    teacher_id = request.GET.get('teacher_id')
    selected_teacher = None
    
    if teacher_id:
        selected_teacher = get_object_or_404(Teacher, pk=teacher_id, organization=request.user)
    elif all_teachers.exists():
        selected_teacher = all_teachers.first()
    
    context = {
        'all_teachers': all_teachers,
        'selected_teacher': selected_teacher
    }
    
    if selected_teacher:
        # Get all results for this teacher's students
        results = Result.objects.filter(
            student__teacher=selected_teacher,
            exam__organization=request.user
        ).select_related('student', 'exam')
        
        # Calculate statistics
        stats = {
            'total_students': selected_teacher.students.count(),
            'total_results': results.count(),
            'avg_percentage': results.aggregate(Avg('percentage'))['percentage__avg'] or 0,
            'avg_band': 0
        }
        
        # Calculate average band score
        if results.exists():
            total_band = sum(result.band_score for result in results)
            stats['avg_band'] = total_band / results.count()
        
        # Score distribution
        score_distribution = [
            {'range': '0-20%', 'count': results.filter(percentage__lt=20).count()},
            {'range': '20-40%', 'count': results.filter(percentage__gte=20, percentage__lt=40).count()},
            {'range': '40-60%', 'count': results.filter(percentage__gte=40, percentage__lt=60).count()},
            {'range': '60-80%', 'count': results.filter(percentage__gte=60, percentage__lt=80).count()},
            {'range': '80-100%', 'count': results.filter(percentage__gte=80).count()},
        ]
        
        # Band distribution
        band_distribution = {}
        for result in results:
            band = result.band_score
            band_distribution[band] = band_distribution.get(band, 0) + 1
        band_distribution = dict(sorted(band_distribution.items()))
        
        # Exam performance - average score per exam
        exam_performance = results.values('exam__title').annotate(
            avg_percentage=Avg('percentage'),
            count=Count('id')
        ).order_by('-avg_percentage')[:10]
        
        # Format exam performance
        exam_performance = [
            {
                'exam_title': item['exam__title'],
                'avg_percentage': round(item['avg_percentage'], 1),
                'count': item['count']
            }
            for item in exam_performance
        ]
        
        # Top students
        top_students = results.order_by('-percentage', '-completed_at')[:5]
        
        # Recent results
        recent_results = results.order_by('-completed_at')[:5]
        
        context.update({
            'stats': stats,
            'score_distribution': score_distribution,
            'band_distribution': band_distribution,
            'exam_performance': exam_performance,
            'top_students': top_students,
            'recent_results': recent_results
        })
    
    return render(request, 'organizations/teacher_statistics.html', context)
