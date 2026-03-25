from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrganizationRegistrationForm, OrganizationLoginForm
from exams.models import Exam
from results.models import Result
from django.db.models import Count, Avg


def register_view(request):
    """Organization registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OrganizationRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Ro\'yxatdan o\'tdingiz! Xush kelibsiz!')
            return redirect('dashboard')
    else:
        form = OrganizationRegistrationForm()
    
    return render(request, 'organizations/register.html', {'form': form})


def login_view(request):
    """Organization login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OrganizationLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Xush kelibsiz, {username}!')
                return redirect('dashboard')
    else:
        form = OrganizationLoginForm()
    
    return render(request, 'organizations/login.html', {'form': form})


@login_required
def logout_view(request):
    """Logout view"""
    logout(request)
    messages.info(request, 'Tizimdan chiqdingiz')
    return redirect('login')


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
    
    recent_results = results.select_related('student', 'exam').order_by('-completed_at')[:10]
    
    context = {
        'total_exams': total_exams,
        'active_exams': active_exams,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 2),
        'recent_results': recent_results,
        'exams': exams[:5]
    }
    
    return render(request, 'organizations/dashboard.html', context)
