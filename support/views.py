from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import SupportVideo, FAQ, ContactInfo, SupportTicket, TeamMember
from .forms import SupportTicketForm


@login_required
def support_view(request):
    """Support page with videos, FAQs, and contact"""
    import json
    
    # Get active support content
    videos = SupportVideo.objects.filter(is_active=True)
    faqs = FAQ.objects.filter(is_active=True)
    contact_info = ContactInfo.objects.filter(is_active=True).first()
    team_members_qs = TeamMember.objects.filter(is_active=True)
    
    # Get user's tickets
    tickets = SupportTicket.objects.filter(organization=request.user).order_by('-created_at')[:5]
    
    # Group videos by category
    videos_by_category = {}
    for video in videos:
        category = video.get_category_display()
        if category not in videos_by_category:
            videos_by_category[category] = []
        videos_by_category[category].append(video)
    
    # Group FAQs by category
    faqs_by_category = {}
    for faq in faqs:
        category = faq.get_category_display()
        if category not in faqs_by_category:
            faqs_by_category[category] = []
        faqs_by_category[category].append(faq)
    
    # Prepare team members data for JavaScript
    team_members_list = [{
        'id': member.id,
        'name': member.name,
        'position': member.position,
        'bio': member.bio,
        'photo': member.photo.url if member.photo else '',
        'email': member.email,
        'telegram': member.telegram,
        'linkedin': member.linkedin,
    } for member in team_members_qs]
    
    context = {
        'videos_by_category': videos_by_category,
        'faqs_by_category': faqs_by_category,
        'contact_info': contact_info,
        'team_members': json.dumps(team_members_list),
        'team_members_list': team_members_qs,  # For template loop
        'tickets': tickets,
    }
    
    return render(request, 'support/support.html', context)


@login_required
def create_ticket_view(request):
    """Create support ticket"""
    if request.method == 'POST':
        form = SupportTicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.organization = request.user
            ticket.save()
            messages.success(request, 'Murojaatingiz muvaffaqiyatli yuborildi! Tez orada javob beramiz.')
            return redirect('support')
        else:
            messages.error(request, 'Xatolik yuz berdi. Iltimos, qaytadan urinib ko\'ring.')
    
    return redirect('support')


@login_required
def ticket_detail_view(request, pk):
    """View ticket details"""
    ticket = get_object_or_404(SupportTicket, pk=pk, organization=request.user)
    
    context = {
        'ticket': ticket,
    }
    
    return render(request, 'support/ticket_detail.html', context)


@login_required
def faq_helpful_view(request, pk):
    """Mark FAQ as helpful - deprecated, keeping for compatibility"""
    messages.success(request, 'Rahmat!')
    return redirect('support')


@login_required
def faq_view_count(request, pk):
    """Increment FAQ view count - deprecated, keeping for compatibility"""
    return redirect('support')
