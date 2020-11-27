from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager
import bcrypt

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
                return redirect('/login/')
        else:
            messages.error(request, "Email not found")
            request.session['type'] = "login"
            return redirect('/login/')
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
            return redirect('/login/')

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
    return redirect('/login/')

def logout(request):
    request.session.flush()
    return redirect('/')