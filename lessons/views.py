from django.shortcuts import render, redirect

def index(request):
    return render(request, 'index.html')

def success(request):
    if 'user_id' in request.session:
        return render(request, 'student_dashboard.html')
    else:
        return redirect('/login/')
    #The order of this if-else mattered...