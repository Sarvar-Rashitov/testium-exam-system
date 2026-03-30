from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Organization


class OrganizationRegistrationForm(UserCreationForm):
    """Organization registration form"""
    full_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    organization_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Organization Name'
    }))
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone Number'
    }))
    
    class Meta:
        model = Organization
        fields = ('full_name', 'email', 'organization_name', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Organization.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Organization.objects.filter(phone=phone).exists():
            raise ValidationError('This phone number is already registered.')
        return phone
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.organization_name = self.cleaned_data['organization_name']
        user.phone = self.cleaned_data['phone']
        # Generate username from email
        user.username = self.cleaned_data['email'].split('@')[0] + str(Organization.objects.count())
        if commit:
            user.save()
        return user


class OrganizationLoginForm(AuthenticationForm):
    """Organization login form"""
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


from .models import OrganizationSettings, Teacher


class ProfileUpdateForm(forms.ModelForm):
    """Profile update form"""
    class Meta:
        model = Organization
        fields = ['full_name', 'organization_name', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'organization_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrganizationSettingsForm(forms.ModelForm):
    """Organization settings form"""
    class Meta:
        model = OrganizationSettings
        exclude = ['organization', 'created_at', 'updated_at']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'primary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'secondary_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_bot_token': forms.TextInput(attrs={'class': 'form-control'}),
            'about_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'mission': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TeacherForm(forms.ModelForm):
    """Teacher form"""
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'phone', 'email', 'subject', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }
