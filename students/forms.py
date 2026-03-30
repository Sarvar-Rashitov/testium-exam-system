from django import forms
from .models import Student
from organizations.models import Teacher


class StudentRegistrationForm(forms.ModelForm):
    """Student registration form before exam"""
    
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        
        # Filter teachers by organization
        if organization:
            self.fields['teacher'].queryset = Teacher.objects.filter(
                organization=organization, 
                is_active=True
            )
        else:
            self.fields['teacher'].queryset = Teacher.objects.none()
    
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'phone', 'telegram_username', 'email', 'student_type', 'teacher')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiya',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567',
                'required': True
            }),
            'telegram_username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'student_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'teacher': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'teacher': "O'qituvchini tanlang"
        }
