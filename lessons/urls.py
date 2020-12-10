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
    path('teacher_choice_double', views.teacher_choice_double),
    path('new_lesson_connect', views.new_lesson_connect),
    path('create_connect_lesson', views.create_connect_lesson),
    path('preview_connect_lesson/<int:lesson_id>', views.preview_connect_lesson),
    path('connect_success', views.connect_success),
    path('post_code/<int:lesson_id>', views.post_code),
    path('get_lesson', views.get_lesson),
    path('update_options', views.update_options),
    path('student_solo/<int:lesson_id>', views.get_solo_lesson),
    path('student_posted/<int:lesson_id>', views.student_posted),
    path('add_like/<int: post_id', views.add_like),
    path('student_work_solo/<int:lesson_id>', views.student_work),
    path('thank_you', views.thank_you),
    path('logout', views.logout)
]