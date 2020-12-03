from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageForm
from .models import Lesson, User

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

        # if user landed here via teacher dashboard form:
        if request.method == "POST":

            # render new lesson screen
            if request.POST['teacher_options'] == "new_lesson":
                return render(request, 'new_lesson.html')

            # redirect to view student work on a lesson
            elif request.POST['teacher_options'] == "student_work":
                return redirect(request, f'lesson/{request.POST.lesson_id}.html')

            # redirect to display lesson code for students
            elif request.POST['teacher_options'] == "post_code":
                return redirect(request, f'lesson/{request.POST.lesson_id}.html')

        # if user clicked "previous screen" on new lesson page:
        else:
            return render(request, 'new_lesson.html')

    else:
        return redirect('/login/')

def new_lesson(request):
    if 'user_id' in request.session:

        if request.GET['lesson_type'] == "open":
            return render(request, 'notice_solo.html')

def solo_lesson_setup(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                new_lesson = form.save(commit=False)
                # save defaults for other settings for now
                # attach the one to many user field data
                new_lesson.user = User.objects.get(id=1)
                new_lesson.save()

                info = {
                    'image' : request.FILES,
                    'heading' : request.POST['heading'],
                    'content' : request.POST['content']
                }
                context = {
                    'info' : info
                }
                return render(request, 'notice_solo.html', context)
            
    else:
        form = ImageForm()
    return render(request, 'notice_solo.html', {'form':form})

# def success(request):
#     context = {
#         'info' : Lesson.objects.last(),
#     }
#     return render(request, 'success.html', context)
#         if request.method == "POST":
#             pass
#     pass
#     return render(request, 'notice_solo.html')

def success(request):
        return HttpResponse("Success!")