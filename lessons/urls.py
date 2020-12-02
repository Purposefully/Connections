from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('student_dashboard', views.student_dashboard),
    path('teacher_dashboard', views.teacher_dashboard),
    path('teacher_choice', views.teacher_choice),
    path('new_lesson', views.new_lesson),
    path('solo_lesson_setup', views.solo_lesson_setup)
]