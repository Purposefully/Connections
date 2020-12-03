from django import forms
from .models import Lesson, User

class ImageForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['image', 'heading', 'content']