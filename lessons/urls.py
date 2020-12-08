from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login/', views.login),
    path('signup', views.signup),
    path('student_dashboard', views.student_dashboard),
    path('single_or_double', views.single_or_double),
    path('teacher_choice_solo', views.teacher_choice_solo),
    path('new_lesson', views.new_lesson),
    path('insert_image', views.insert_image),
    path('update_words', views.update_words),
    path('update_settings', views.update_settings),
    path('preview_solo_lesson/<int:lesson_id>', views.preview_solo_lesson),
    path('revise_solo', views.revise_solo),
    path('success', views.success),
    path('post_code/<int:lesson_id>', views.post_code)
]