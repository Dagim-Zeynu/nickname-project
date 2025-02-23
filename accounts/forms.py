from django import forms
from .models import Profile, Department
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.db import transaction
from django.contrib.auth.models import User
import uuid

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'department']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }

class CustomSignupForm(SignupForm):
    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-purple-500 focus:border-purple-500',
                'placeholder': 'Enter your full name'
            }
        )
    )
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by('name'),
        widget=forms.Select(
            attrs={
                'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-purple-500 focus:border-purple-500'
            }
        )
    )

    terms = forms.BooleanField(
        required=True,
        error_messages={
            'required': 'You must agree to the Terms and Conditions'
        }
    )

    def save(self, request):
        # Generate a unique username from email
        email = self.cleaned_data.get('email')
        username = email.split('@')[0]
        if len(username) > 30:  # Django username max length is 150
            username = username[:30]
        
        # Add a unique identifier if username exists
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Set the username
        self.cleaned_data['username'] = username
        
        # Save the user
        with transaction.atomic():
            user = super().save(request)
            try:
                profile = Profile.objects.create(
                    user=user,
                    full_name=self.cleaned_data.get('full_name', ''),
                    department=self.cleaned_data.get('department'),
                    registration_complete=True
                )
            except Exception as e:
                user.delete()
                raise forms.ValidationError('Error creating profile. Please try again.')
            
            return user

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('full_name'):
            raise forms.ValidationError('Full name is required')
        if not cleaned_data.get('department'):
            raise forms.ValidationError('Department is required')
        return cleaned_data 