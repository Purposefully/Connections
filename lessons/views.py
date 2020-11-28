from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def student_dashboard(request):
    if 'user_id' in request.session:
        return render(request, 'student_dashboard.html')
    else:
        return redirect('/login/')

def teacher_dashboard(request):
    if 'user_id' in request.session:
        return render(request, 'teacher_dashboard.html')
    else:
        return redirect('/login/')

def teacher_choice(request):
    if 'user_id' in request.session:

        # render new lesson screen
        if request.GET['teacher_options'] == "new_lesson":
            return render(request, 'new_lesson.html')

        # redirect to view student work on a lesson
        elif request.GET['teacher_options'] == "student_work":
            return redirect(request, f'lesson/{request.GET.lesson_id}.html')

        # redirect to display lesson code for students
        elif request.GET['teacher_options'] == "post_code":
            return redirect(request, f'lesson/{request.GET.lesson_id}.html')


    else:
        return redirect('/login/')

# def new_lesson(request):
#     if 'user_id' in request.session:
#         if request.method == "POST":
#             pass
#         return render(request, 'new_lesson.html')