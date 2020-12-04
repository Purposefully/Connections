from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ImageForm
from django.contrib import messages
from .models import *
import bcrypt

# Home page
def index(request):
    return render(request, 'index.html')

# Login and Registration
def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user: 
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                # For future reference, we had to add the .id to the line above to make it work
                return redirect('/student_dashboard')
            else:
                messages.error(request, "Incorrect password")
                return redirect('/login')
        else:
            messages.error(request, "Email not found")
            request.session['type'] = "login"
            return redirect('/login')
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":

        errors = User.objects.basic_validator(request.POST)

        # Check to make sure email is not already in db
        duplicate = User.objects.filter(email=request.POST['email'])
        if duplicate:
            errors['registered'] = "A user account already exists with that email."

        if errors:
            for k, v in errors.items():
                messages.error(request, v)
            request.session['name'] = request.POST['name']
            request.session['email'] = request.POST['email']
            request.session['type'] = "signup"
            return redirect('/login')

        #if no errors, add user to database
        pwdhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            password = pwdhash
        )
        # Remove entries from screen
        request.session.flush()
        request.session['user_id'] = User.objects.last().id
        return redirect('/student_dashboard')
    return redirect('/login')

def logout(request):
    request.session.flush()
    return redirect('/')


# Options
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
            form = ImageForm()
            return render(request, 'notice_solo.html', {'form':form})

def solo_lesson_setup(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)

            if form.is_valid():
                new_lesson = form.save(commit=False)
                # save defaults for other settings for now
                # attach the one to many user field data
                new_lesson.user = User.objects.get(id=request.session['user_id'])
                new_lesson.save()

                context = {
                    'info' : new_lesson
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