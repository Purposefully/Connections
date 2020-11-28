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
        return redirect(request, 'notice_solo.html')
    else:
        return redirect('/login/')