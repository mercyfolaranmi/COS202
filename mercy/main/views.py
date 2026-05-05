from urllib import request

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .cgpa_utils import calculate_gpa
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()  # <-- Use this instead of importing User directly


def login_view(request):
    if request.method == 'POST':
        matric = request.POST.get('matric')
        password = request.POST.get('password')
        request.session['matric'] = matric
        return redirect('dashboard')
    return render(request, 'index.html')


@login_required
def dashboard_view(request):
    return render(request, 'account/dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        matric = request.POST.get('matric')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('signup')
        
        if User.objects.filter(username=matric).exists():
            messages.error(request, 'Matric number already registered!')
            return redirect('signup')
        
        user = User.objects.create_user(username=matric, password=password)
        user.save()

        messages.success(request, 'Account created! Please log in.')
        return redirect('login')
    
    return render(request, 'account/signup.html')


@login_required
def download_cgpa_pdf(request):
    pass


def cgpa_calculator_view(request):
    if request.method == 'POST':
        student_info = {
            'name': request.POST.get('name'),
            'level': request.POST.get('level'),
            'matric': request.POST.get('matric'),
            'programme': request.POST.get('programme'),
            'faculty': request.POST.get('faculty'),
            'department': request.POST.get('department'),
            'date': request.POST.get('date'),
        }
        
        num_courses = int(request.POST.get('num_courses', 0))
        courses_data = []
        
        for i in range(1, num_courses + 1):
            course_name = request.POST.get(f'course_name_{i}')
            credit_unit = request.POST.get(f'credit_unit_{i}')
            score = request.POST.get(f'score_{i}')
            
            if course_name and credit_unit and score:
                courses_data.append({
                    'name': course_name,
                    'credit_unit': int(credit_unit),
                    'score': int(score)
                })
        
        result = calculate_gpa(courses_data)
        
        context = {
            'student_info': student_info,
            'result': result,
            'courses': result['course_results']
        }
        
        return render(request, 'account/cgpa_result.html', context)
    
    return render(request, 'account/cgpa_form.html')