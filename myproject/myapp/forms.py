from django import forms
from .models import message, Feedback

class PostForm(forms.ModelForm):
    class Meta:
        model = message
        fields = ['title', 'description', 'image']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your feedback message...', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }