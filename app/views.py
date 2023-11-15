from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_process, logout 
from .forms import UserCreationForm, LoginForm, SignupForm
from django.contrib import messages
# Create your views here.

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

# def index(request):
#     return render(request, 'index.html')

# signup page
def user_signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'sign_up.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login_process(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')