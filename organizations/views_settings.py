from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Organization, OrganizationSettings
from .forms import OrganizationSettingsForm, ProfileUpdateForm


@login_required
def settings_view(request):
    """Settings page with tabs"""
    # Get or create settings
    settings, created = OrganizationSettings.objects.get_or_create(organization=request.user)
    
    active_tab = request.GET.get('tab', 'profile')
    
    context = {
        'settings': settings,
        'active_tab': active_tab,
    }
    
    return render(request, 'organizations/settings.html', context)


@login_required
def update_profile_view(request):
    """Update organization profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
            return redirect('settings')
        else:
            messages.error(request, 'Xatolik yuz berdi. Iltimos, qaytadan urinib ko\'ring.')
    
    return redirect('settings')


@login_required
def update_settings_view(request):
    """Update organization settings"""
    settings, created = OrganizationSettings.objects.get_or_create(organization=request.user)
    
    if request.method == 'POST':
        # Determine which tab we're updating
        tab = 'branding'
        
        # Handle logo upload
        if 'logo' in request.FILES:
            settings.logo = request.FILES['logo']
            settings.save()
            messages.success(request, 'Logo muvaffaqiyatli yuklandi!')
            return redirect(f'/settings/?tab={tab}')
        
        # Handle notifications
        if 'email_notifications' in request.POST or 'telegram_notifications' in request.POST:
            settings.email_notifications = 'email_notifications' in request.POST
            settings.telegram_notifications = 'telegram_notifications' in request.POST
            settings.telegram_bot_token = request.POST.get('telegram_bot_token', '')
            settings.save()
            messages.success(request, 'Xabarnoma sozlamalari saqlandi!')
            tab = 'notifications'
            return redirect(f'/settings/?tab={tab}')
        
        # Handle other settings
        form = OrganizationSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sozlamalar muvaffaqiyatli saqlandi!')
            return redirect(f'/settings/?tab={tab}')
        else:
            messages.error(request, 'Xatolik yuz berdi. Iltimos, qaytadan urinib ko\'ring.')
    
    return redirect('/settings/')


@login_required
def change_password_view(request):
    """Change password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Parol muvaffaqiyatli o\'zgartirildi!')
            return redirect('/settings/?tab=security')
        else:
            for error in form.errors.values():
                messages.error(request, str(error[0]))
            return redirect('/settings/?tab=security')
    
    return redirect('/settings/?tab=security')
