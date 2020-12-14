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
                request.session['type'] = "login"
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
            lesson_id = request.POST['lesson']

            # render lesson screen for making changes or deleting the lesson
            if request.POST['action'] == "modify":
                return redirect(f'/revise_solo/{lesson_id}')

            # redirect to view student work on a lesson
            elif request.POST['action'] == "student_work":
                return redirect(f'student_work_solo/{lesson_id}')

            # redirect to display lesson code for students
            elif request.POST['action'] == "code":
                request.session['type'] = 'single'

                # make sure lesson settings are updated for teacher's request
                this_lesson = Solo_Lesson.objects.get(id=lesson_id)
                if request.POST['parts'] == "part_1":
                    this_lesson.like_same_day = False
                    this_lesson.save()

                else:
                    this_lesson.like_same_day = True
                    this_lesson.save()

                print("The lesson id is", lesson_id)
                return redirect(f'post_code/{lesson_id}')

        # if user clicked "previous screen" on new lesson page or got here from single or double
        else:
            context = {
                'lessons': User.objects.get(id=request.session['user_id']).solo_lessons.all()
            }
            return render(request, 'new_lesson_solo.html', context)

    else:
        return redirect('/login/')

def update_options(request):
    return render(request, 'today_option.html')

def teacher_choice_double(request):
    if 'user_id' in request.session:

        if request.method == "POST":
            lesson_id = request.POST['lesson']

            print(request.POST)
            # render new lesson screen
            if request.POST['action'] == "modify":
                context = {
                    'lesson': Connect_Lesson.objects.get(id=request.POST['lesson'])
                }
                return redirect(f'revise_connect/{lesson_id}')

            # redirect to view student work on a lesson
            elif request.POST['action'] == "student_work":
                lesson_id = request.POST['lesson']
                return redirect(f'student_work_connect/{lesson_id}')

            # redirect to display lesson code for students
            elif request.POST['action'] == "code":
                lesson_id = request.POST['lesson']
                request.session['type'] = 'connect'

                # make sure lesson settings are updated for teacher's request
                this_lesson = Connect_Lesson.objects.get(id=lesson_id)
                if request.POST['parts'] == "part_1":
                    this_lesson.like_same_day = False
                    this_lesson.save()

                else:
                    this_lesson.like_same_day = True
                    this_lesson.save()

                print("The lesson id is", lesson_id)
                return redirect(f'post_code/{lesson_id}')

        # if user got here from elsewhere
        else:
            context = {
                'solo_lessons': User.objects.get(id=request.session['user_id']).solo_lessons.all(),
                'connect_lessons': User.objects.get(id=request.session['user_id']).connect_lessons.all()
            }
            return render(request, 'new_connect_lesson.html', context)

# Creating/Revising Lessons
# Single Image Lessons

def new_lesson(request):
    if 'user_id' in request.session:

        context = {
            'img_form': ImageForm(),
            'list': [0,1,2,3,4,5]
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
                    this_lesson.max_likes = request.POST['number_likes']
            else:
                this_lesson.likes_allowed = False
                this_lesson.max_likes = 0

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
            this_lesson.lesson_code = get_random_string(length=6)
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

def revise_solo(request, lesson_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            print(request.POST)
            this_lesson = Solo_Lesson.objects.get(id=lesson_id)
            if 'likes_allowed' in request.POST:
                if request.POST['likes_allowed'] == 'on':
                    this_lesson.likes_allowed = True
                    this_lesson.max_likes = request.POST['number_likes']
            else:
                this_lesson.likes_allowed = False
                this_lesson.max_likes = 0

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

            this_lesson.justification_text = request.POST['prompt']
            this_lesson.title = request.POST['title']
            this_lesson.save()

            return redirect(f"/preview_solo_lesson/{this_lesson.id}")


        else:
            lesson = Solo_Lesson.objects.get(id=lesson_id)
            likes = justification = same_day = False
            if lesson.likes_allowed == True:
                likes = "checked"

            if lesson.justification_required == True:
                justification = "checked"

            if lesson.like_same_day == True:
                same_day = "checked"
            print(lesson.likes_allowed, lesson.justification_required, lesson.like_same_day, lesson.max_likes)
            print(likes, justification, same_day)
            context = {
                'info': Solo_Lesson.objects.get(id=lesson_id),
                'likes': likes,
                'max_likes' : lesson.max_likes,
                'justification': justification,
                'same_day': same_day,
                'list': [0,1,2,3,4,5],
                'connect_lessons': lesson.connect_lessons.all()
            }
    return render(request, 'revise_solo.html', context)

def success(request, lesson_id):
    if 'user_id' in request.session:
        context = {
            'lesson': Solo_Lesson.objects.get(id=lesson_id)
        }
        return render(request, 'success.html', context)

def delete_lesson(request, lesson_id):
    if 'user_id' in request.session:
        this_lesson = Solo_Lesson.objects.get(id=lesson_id)
        # Get any connect lessons that use this solo lesson
        # Delete them, too.
        this_lesson.connect_lessons.all().delete()
        this_lesson.delete()

    return redirect('/single_or_double')

def duplicate_lesson(request, lesson_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            lesson = Solo_Lesson.objects.get(id=lesson_id)
            lesson.id = None
            lesson.title = request.POST['title']
            lesson.lesson_code = get_random_string(length=6)
            lesson.save()
            return redirect(f"/revise_solo/{lesson.id}")

def post_code(request, lesson_id):
    if 'user_id' in request.session:
        if request.session['type'] == "connect":
            print("in the connect lessons")
            context = {
                'lesson': Connect_Lesson.objects.get(id=lesson_id)
            }
        else:
            print("in the solo lessons")
            context = {
                'lesson': Solo_Lesson.objects.get(id=lesson_id)
            }
        return render(request, 'code.html', context)

def student_work(request, lesson_id):
    if 'user_id' in request.session:
        this_lesson = Solo_Lesson.objects.get(id=lesson_id)
        posts = Post.objects.filter(solo_lesson=this_lesson)

        context = {
            'lesson': this_lesson,
            'posts': posts
        }
        return render(request, 'student_work_solo.html', context)

# Creating/Revising Lessons
# Connect 2 Images Lessons

def new_lesson_connect(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            # returns lesson ids in an array
            # to see it:
            # print(request.POST.getlist('lessons'))
            lessons = request.POST.getlist('lessons')

            lesson1 = Solo_Lesson.objects.get(id=lessons[0])
            lesson2 = Solo_Lesson.objects.get(id=lessons[1])
            context = {
                'lesson1':lesson1,
                'posts1': Post.objects.filter(solo_lesson=lesson1),
                'lesson2': lesson2,
                'posts2': Post.objects.filter(solo_lesson=lesson2),
                'list': [0,1,2,3,4,5]
            }
            return render(request, 'notice_connect.html', context)

def create_connect_lesson(request):
    if 'user_id' in request.session:
        if request.method == "POST":
            print(request.POST)

            if 'likes_allowed' in request.POST:
                if request.POST['likes_allowed'] == 'on':
                    likes_allowed = True
            else:
                likes_allowed = False

            if 'justification_required' in request.POST:
                if request.POST['justification_required'] == 'on':
                    justification_required = True
            else:
                justification_required = False

            if 'like_same_day' in request.POST:
                if request.POST['like_same_day'] == 'on':
                    like_same_day = True
            else:
                like_same_day= False

            this_lesson = Connect_Lesson.objects.create(
                title = request.POST['title'],
                heading = request.POST['heading'],
                content = request.POST['content'],
                likes_allowed = likes_allowed,
                max_likes = request.POST['number_likes'],
                justification_required = justification_required,
                justification_text = request.POST['prompt'],
                like_same_day = like_same_day,
                lesson_code = get_random_string(length=6),
                user = User.objects.get(id=request.session['user_id']),
            )

            lesson1 = Solo_Lesson.objects.get(id=request.POST['lesson1'])
            this_lesson.lessons.add(lesson1)
            lesson2 = Solo_Lesson.objects.get(id=request.POST['lesson2'])
            this_lesson.lessons.add(lesson2)

            return redirect(f"/preview_connect_lesson/{this_lesson.id}")

    return redirect(request, '/login/')

def preview_connect_lesson(request, lesson_id):
    if 'user_id' in request.session:
        # lesson = Connect_Lesson.objects.get(id=lesson_id)
        # print(lesson.likes_allowed, lesson.justification_required, lesson.like_same_day)

        this_connect_lesson = Connect_Lesson.objects.get(id=lesson_id)
        single_lessons = this_connect_lesson.lessons.all()
        print(single_lessons[0])
        print(single_lessons[1])

        context = {
            'connect_lesson': this_connect_lesson,
            'solo_lesson1':single_lessons[0],
            'posts1': Post.objects.filter(solo_lesson=single_lessons[0]),
            'solo_lesson2': single_lessons[1],
            'posts2': Post.objects.filter(solo_lesson=single_lessons[1]),
        }

        request.session['type'] = 'connect'
        return render(request, 'connect_preview.html', context)

def revise_connect(request, lesson_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            print(request.POST)
            this_lesson = Connect_Lesson.objects.get(id=lesson_id)
            if 'likes_allowed' in request.POST:
                if request.POST['likes_allowed'] == 'on':
                    this_lesson.likes_allowed = True
                    this_lesson.max_likes = request.POST['number_likes']
            else:
                this_lesson.likes_allowed = False
                this_lesson.max_likes = 0

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

            this_lesson.justification_text = request.POST['prompt']
            this_lesson.title = request.POST['title']
            this_lesson.save()

            return redirect(f"/preview_connect_lesson/{this_lesson.id}")


        else:
            this_lesson = Connect_Lesson.objects.get(id=lesson_id)
            print(this_lesson.__dict__)
            likes = justification = same_day = False
            if this_lesson.likes_allowed == True:
                likes = "checked"

            if this_lesson.justification_required == True:
                justification = "checked"

            if this_lesson.like_same_day == True:
                same_day = "checked"
            # print(lesson.likes_allowed, lesson.justification_required, lesson.like_same_day, lesson.max_likes)
            # print(likes, justification, same_day)
            single_lessons = this_lesson.lessons.all()
            print(single_lessons[0])
            print(single_lessons[1])

        context = {
            'connect_lesson': this_lesson,
            'solo_lesson1':single_lessons[0],
            'posts1': Post.objects.filter(solo_lesson=single_lessons[0]),
            'solo_lesson2': single_lessons[1],
            'posts2': Post.objects.filter(solo_lesson=single_lessons[1]),
            'likes': likes,
            'max_likes' : this_lesson.max_likes,
            'justification': justification,
            'same_day': same_day,
            'list': [0,1,2,3,4,5]
        }

        return render(request, 'revise_connect.html', context)

def connect_success(request, lesson_id):
    if 'user_id' in request.session:

        context = {
            'lesson': Connect_Lesson.objects.get(id=lesson_id)
        }
        return render(request, 'connect_success.html', context)

def delete_connect_lesson(request, lesson_id):
    if 'user_id' in request.session:
        Connect_Lesson.objects.get(id=lesson_id).delete()
    return redirect('/single_or_double')

def duplicate_connect_lesson(request, lesson_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            lesson = Connect_Lesson.objects.get(id=lesson_id)
            # get the single lessons in the many-to-many field
            single_lessons = lesson.lessons.all()
            lesson.id = None
            lesson.title = request.POST['title']
            lesson.lesson_code = get_random_string(length=6)
            lesson.save()
            # add the single lessons to the many-to-many field of duplicated lesson
            lesson.lessons.set(single_lessons)
            return redirect(f"/revise_connect/{lesson.id}")

# Student Actions

def get_lesson(request):
    if 'user_id' in request.session:
        # check for valid code
        # check whether code in single or double lesson DB
        # return redirect with lesson id number to proper page
        if request.method == "POST":
            lessons = Solo_Lesson.objects.filter(lesson_code = request.POST['code'])
            lessons2 = Connect_Lesson.objects.filter(lesson_code = request.POST['code'])
            if lessons:
                if lessons[0].lesson_code != '':
                    this_lesson = lessons[0]
                    return redirect(f'/student_solo/{this_lesson.id}')
            elif lessons2 :
                if lessons2:
                    if lessons2[0].lesson_code != '':
                        this_lesson = lessons2[0]
                    return redirect(f'/student_connect/{this_lesson.id}')
            else:
                print("makes it here")
                messages.error(request, "Please check you typed that code correctly...")
                print(messages)

        return redirect('/student_dashboard')

def get_solo_lesson(request, lesson_id):
    if 'user_id' in request.session:

        this_lesson = Solo_Lesson.objects.get(id=lesson_id)
        posts = Post.objects.filter(solo_lesson=this_lesson)
        this_user = User.objects.get(id=request.session['user_id'])

        # Check how many likes user has selected for posts in this lesson
        liked_posts = []
        for post in posts:
            liked_posts += (list(Like.objects.filter(post=post, user=this_user)))
        # print("liked posts", liked_posts)
        num_likes = len(liked_posts)
        print("number of likes", num_likes)
        request.session['num_likes'] = num_likes

        context = {
            'lesson': this_lesson,
            'posts': posts,
            'user': this_user,
            'likes': Like.objects.filter(user=this_user),
            'num_likes': num_likes
        }

        # Check to see if student already posted on this lesson

        this_users_posts = Post.objects.filter(user=this_user,solo_lesson=lesson_id)

        if this_users_posts:
            if this_users_posts[0].content != '':
                return render(request, 'notice_class.html', context)
        else:
            return render(request, 'student_solo.html', context)
    return redirect('/')

def student_posted(request, lesson_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            # save post to the database
            this_user = User.objects.get(id=request.session['user_id'])
            this_lesson = Solo_Lesson.objects.get(id=lesson_id)
            Post.objects.create(
                content = request.POST['content'],
                user = this_user,
                solo_lesson = this_lesson
            )
            # send student somewhere
            print("like same day", this_lesson.like_same_day)
            if this_lesson.like_same_day == False:
                return redirect('/thank_you')
            else:
                return redirect(f'/student_solo/{this_lesson.id}')

                # posts = Post.objects.filter(solo_lesson=this_lesson)
                # # Check how many likes user has selected for posts in this lesson
                # liked_posts = []
                # for post in posts:
                #     liked_posts += (list(Like.objects.filter(post=post, user=this_user)))
                # # print("liked posts", liked_posts)
                # num_likes = len(liked_posts)
                # # print("number of likes", num_likes)
                # request.session['num_likes'] = num_likes
                # context = {
                #     'lesson': this_lesson,
                #     'posts': Post.objects.filter(solo_lesson=this_lesson),
                #     'user': this_user,
                #     'likes': Like.objects.filter(user=this_user),
                #     'num_likes': num_likes
                # }
                # return redirect(request, 'notice_class.html', context)
    return redirect('/')

def add_like(request):
    if 'user_id' in request.session:
        if request.method == "POST":

            print(request.POST)
            # Create like
            this_user = User.objects.get(id=request.session['user_id'])
            this_post = Post.objects.get(id=request.POST['post_id'])
            Like.objects.create(
                justification = request.POST['justification'],
                user = this_user,
                post = this_post
            )

            # Check how many likes user has selected for posts in this lesson
            this_lesson_id = this_post.solo_lesson.id
            these_posts = Post.objects.filter(solo_lesson=this_lesson_id)
            liked_posts = []
            for post in these_posts:
                liked_posts += (list(Like.objects.filter(post=post, user=this_user)))
            # print("liked posts", liked_posts)
            num_likes = len(liked_posts)
            print("number of likes", num_likes)

            if num_likes >= Solo_Lesson.objects.get(id=this_lesson_id).max_likes:
                context = {
                    'num_likes': num_likes
                }
                return render(request, 'finished_selecting.html', context)
            else:
                context = {
                    'post': this_post,
                    'user': this_user,
                    'likes': Like.objects.filter(user=this_user),
                    'num_likes': num_likes
                }
                return render(request, 'update_likes.html', context)

def get_connect_lesson(request, lesson_id):
    if 'user_id' in request.session:

        this_connect_lesson = Connect_Lesson.objects.get(id=lesson_id)
        single_lessons = this_connect_lesson.lessons.all()
        print(single_lessons[0])
        print(single_lessons[1])

        connect_posts = ConnectPost.objects.filter(connect_lesson=this_connect_lesson)
        this_user = User.objects.get(id=request.session['user_id'])

        context = {
            'lesson': this_connect_lesson,
            'solo_lesson1':single_lessons[0],
            'posts1': Post.objects.filter(solo_lesson=single_lessons[0]),
            'solo_lesson2': single_lessons[1],
            'posts2': Post.objects.filter(solo_lesson=single_lessons[1]),
            'connect_posts': connect_posts,
            'user': this_user
        }

        # Check to see if student already posted on this lesson

        this_users_posts = ConnectPost.objects.filter(user=this_user,connect_lesson=lesson_id)

        if this_users_posts:
            if this_users_posts[0].content != '':
                return render(request, 'class_connect.html', context)
        else:
            return render(request, 'student_connect.html', context)
    return redirect('/')

def student_posted_connect(request, lesson_id):
    if 'user_id' in request.session:
        if request.method == "POST":
            # save post to the database
            this_user = User.objects.get(id=request.session['user_id'])
            this_lesson = Connect_Lesson.objects.get(id=lesson_id)
            ConnectPost.objects.create(
                content = request.POST['content'],
                user = this_user,
                connect_lesson = this_lesson
            )
            # send student somewhere
            if this_lesson.like_same_day == False:
                return redirect('/thank_you')
            else:
                return redirect(f'/student_connect/{this_lesson.id}')
                # single_lessons = this_lesson.lessons.all()
                # context = {
                #     'lesson': this_lesson,
                #     'solo_lesson1':single_lessons[0],
                #     'posts1': Post.objects.filter(solo_lesson=single_lessons[0]),
                #     'solo_lesson2': single_lessons[1],
                #     'posts2': Post.objects.filter(solo_lesson=single_lessons[1]),
                #     'connect_posts': ConnectPost.objects.filter(connect_lesson=this_lesson),
                #     'user': this_user
                # }
                # return render(request, 'connect_class.html', context)
    return redirect('/')

def thank_you(request):
    return render(request, 'thank_you.html')