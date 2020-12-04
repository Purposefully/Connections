from django import forms
from .models import Solo_Lesson, User

class ImageForm(forms.ModelForm):
    class Meta:
        model = Solo_Lesson
        fields = ['image', 'heading', 'content']