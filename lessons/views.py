from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import messages
from .models import *
import bcrypt
from django.utils.crypto import get_random_string

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

def single_or_double(request):
    if 'user_id' in request.session:
        return render(request, 'single_or_double.html')
    else:
        return redirect('/login/')

def teacher_choice_solo(request):
    if 'user_id' in request.session:

        if request.method == "POST":

            # render new lesson screen
            if request.POST['action'] == "modify":
                context = {
                    'lesson': Solo_Lesson.objects.get(id=request.POST['lesson'])
                }
                return render(request, 'revise_solo.html', context)

            # redirect to view student work on a lesson
            elif request.POST['action'] == "student_work":
                return redirect(f'lesson/{request.POST.lesson_id}.html')

            # redirect to display lesson code for students
            elif request.POST['action'] == "code":
                lesson_id = request.POST['lesson']
                print("The lesson id is", lesson_id)
                return redirect(f'post_code/{lesson_id}')

        # if user clicked "previous screen" on new lesson page or got here from 
        else:
            context = {
                'lessons': User.objects.get(id=request.session['user_id']).solo_lessons.all()
            }
            return render(request, 'new_lesson_solo.html', context)

    else:
        return redirect('/login/')


# Creating/Revising Lessons

def new_lesson(request):
    if 'user_id' in request.session:

        context = {
            'img_form': ImageForm(),
        }
        return render(request, 'notice_solo.html', context)

def insert_image(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            form = ImageForm(request.POST, request.FILES)
            print(request.FILES)

            if form.is_valid():
                print("form is valid")
                new_lesson = form.save(commit=False)
                # save defaults for other settings for now
                # attach the one to many user field data
                new_lesson.user = User.objects.get(id=request.session['user_id'])
                new_lesson.save()

                request.session['current_lesson'] = new_lesson.id
                print(request.session['current_lesson'])

                context = {
                    'info' : new_lesson,
                }
                return render(request, 'display_image.html', context)

        else:
            print("nope, not valid")
            form = ImageForm()
        print("this is where it ends up")
        return render(request, 'notice_solo.html', {'form':form})

def update_words(request):
    if 'user_id' in request.session:
        if request.method == "POST":

            print(request.POST)
            print(request.session['current_lesson'])
            print("getting here")
            this_lesson = Solo_Lesson.objects.get(id=request.POST['solo_lesson_id'])

            if 'heading' in request.POST:
                print("inside heading branch")
                this_lesson.heading = request.POST['heading']
                this_lesson.save()
                context = {
                    'info' : this_lesson
                }
                return render(request, 'update_heading.html', context)

            if 'content' in request.POST:
                this_lesson.content = request.POST['content']
                this_lesson.save()

                print(this_lesson.heading)

                context = {
                    'info' : this_lesson
                }
                return render(request, 'update_directions.html', context)

        else:
            form = ImageForm()

    return render(request, 'notice_solo.html', {'form':form})

def update_settings(request):
    if 'user_id' in request.session:
        print("it does get here")
        if request.method == "POST":
            print(request.POST)
            this_lesson = Solo_Lesson.objects.get(id=request.session['current_lesson'])

            if 'likes_allowed' in request.POST:
                if request.POST['likes_allowed'] == 'on':
                    this_lesson.likes_allowed = True
                else:
                    this_lesson.likes_allowed = False

            if 'justification_required' in request.POST:
                    if request.POST['justification_required'] == 'on':
                        this_lesson.justification_required = True
                    else:
                        this_lesson.justification_required = False

            if 'like_same_day' in request.POST:
                    if request.POST['like_same_day'] == 'on':
                        this_lesson.like_same_day = True
                    else:
                        this_lesson.like_same_day= False

            this_lesson.max_likes = request.POST['number_likes']
            this_lesson.justification_text = request.POST['prompt']
            this_lesson.title = request.POST['title']
            this_lesson.save()

            return redirect(f"/preview_solo_lesson/{this_lesson.id}")

    return redirect(request, '/login/')

def preview_solo_lesson(request, lesson_id):
    if 'user_id' in request.session:
        lesson = Solo_Lesson.objects.get(id=lesson_id)
        print(lesson.likes_allowed, lesson.justification_required, lesson.like_same_day)
        context = {
            'lesson': Solo_Lesson.objects.get(id=lesson_id)
        }
        return render(request, 'solo_preview.html', context)

def revise_solo(request):
    if 'user_id' in request.session:
        lesson = Solo_Lesson.objects.last()
        likes = justification = same_day = False
        if lesson.likes_allowed == True:
            likes = "checked"

        if lesson.justification_required == True:
            justification = "checked"

        if lesson.like_same_day == True:
            same_day = "checked"
        print(lesson.likes_allowed, lesson.justification_required, lesson.like_same_day)
        print(likes, justification, same_day)
        context = {
            'info': Solo_Lesson.objects.last(),
            'likes': likes,
            'justification': justification,
            'same_day': same_day
        }
    return render(request, 'revise_solo.html', context)

def success(request):
    if 'user_id' in request.session:
        lesson = Solo_Lesson.objects.last()
        lesson.lesson_code = get_random_string(length=10)
        lesson.save()

        context = {
            'lesson': lesson
        }
        return render(request, 'success.html', context)

def post_code(request, lesson_id):
    if 'user_id' in request.session:
        context = {
            'lesson': Solo_Lesson.objects.get(id=lesson_id)
        }
        return render(request, 'code.html', context)

# Student Actions

def get_lesson(request):
    if 'user_id' in request.session:
        # check for valid code
        # check whether code in single or double lesson DB
        # return redirect with lesson id number to proper page
        if request.method == "POST":
            lessons = Solo_Lesson.objects.filter(lesson_code = request.POST['code'])
            if lessons:
                if lessons[0].lesson_code != '':
                    this_lesson = lessons[0]
                    return redirect(f'/student_solo/{this_lesson.id}')
            elif (False):
                #check double lesson DB
                pass
            else:
                print("makes it here")
                messages.error(request, "Please check you typed that code correctly...")
                print(messages)

        return redirect('/student_dashboard')

def get_solo_lesson(request, lesson_id):
    if 'user_id' in request.session:
        context = {
            'lesson': Solo_Lesson.objects.get(id=lesson_id)
        }
        return render(request, 'student_solo.html', context)
    return redirect('/')

def student_posted(request, lesson_id):
    if 'user_id' in request.session:
        # save post to the database
        this_user = User.objects.get(id=request.session['user_id'])
        this_lesson = Solo_Lesson.objects.get(id=lesson_id)
        Post.objects.create(
            content = request.POST['content'],
            user = this_user,
            solo_lesson = this_lesson
        )
        # send student somewhere
        return redirect('/thank_you')
    return redirect('/')

def thank_you(request):
    return render(request, 'thank_you.html')