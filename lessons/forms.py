from django import forms
from .models import Solo_Lesson, User

class ImageForm(forms.ModelForm):
    class Meta:
        model = Solo_Lesson
        fields = ['image']

class HeadingForm(forms.ModelForm):
    class Meta:
        model = Solo_Lesson
        fields = ['heading']

class ContentForm(forms.ModelForm):
    class Meta:
        model = Solo_Lesson
        fields = ['content']