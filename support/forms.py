from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):
    """Support ticket form"""
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message', 'category', 'priority', 'attachment']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Muammo yoki savol mavzusi'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Batafsil ma\'lumot bering...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,.pdf,.doc,.docx'
            }),
        }
