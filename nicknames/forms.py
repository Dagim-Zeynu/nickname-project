from django import forms
from .models import Nickname

class NicknameForm(forms.ModelForm):
    class Meta:
        model = Nickname
        fields = ['nickname', 'reason']
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter nickname'
            }),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why this nickname?'
            }),
        }

class RatingForm(forms.ModelForm):
    score = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(
            attrs={
                'class': 'appearance-none block w-20 px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-purple-500 focus:border-purple-500',
                'min': '1',
                'max': '10'
            }
        )
    )

    