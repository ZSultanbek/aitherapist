from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type', 'guest')

        if password == password2:
            if User.objects.filter(username=username).exists():
                context = {'error': 'Username already exists.'}
                return render(request, 'accounts/register.html', context)
            else:
                user = User.objects.create_user(username=username, password=password, user_type=user_type)
                user.save()
                context = {'success': 'User registered successfully.'}
                return render(request, 'accounts/register.html', context)
        else:
            context = {'error': 'Passwords do not match.'}
            return render(request, 'accounts/register.html', context)

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            context = {'success': 'Logged in successfully.'}
            return redirect('home') 
        else:
            context = {'error': 'Invalid username or password.'}
            return render(request, 'accounts/login.html', context)
        
    


    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    context = {'success': 'Logged out successfully.'}
    return render(request, 'accounts/login.html', context)