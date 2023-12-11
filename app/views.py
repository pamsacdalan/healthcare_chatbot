from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_process, logout 
from .forms import UserCreationForm, LoginForm, SignupForm
from django.contrib import messages
from dotenv import load_dotenv


from django.http import JsonResponse
from .models import Chat, Dentist_Schedule, UserAddress
from datetime import datetime
from chatbot.local_history import chain
from chatbot.model.gptbot import gptbot
from chatbot.model.db_fetch import text_to_sql 
from chatbot.langsql.converted_functions.appointment import *

from psycopg2 import Error
# Create your views here.


def login(request):
    return render(request, 'login.html')

def home(request):
    chats = Chat.objects.filter(user=request.user)
    user = User.objects.get(username=request.user.username)
    print(user.username)
    print(user.id)
    location = UserAddress.objects.get(username_id=user.username)
    print(location.city)
        
    if request.method == 'POST':
        message = request.POST.get('message')
        
        if "list" or "how many" in message:
            """Sets appointment using series of questions. Returns sql INSERT statement."""
            response = text_to_sql(message)
            now = datetime.now()
            date_time_string = now.strftime("%m/%d/%Y %H:%M:%S")
            chat = Chat(user=request.user, message=message, response=response, created_at=date_time_string)
            chat.save()
            return JsonResponse({'message': message, 'response': response, 'created_at': date_time_string})
        
        elif "set appointment" in message:
            response = 'Please specify your appointment details'
            return JsonResponse({'message': message, 'response': response, 'created_at': date_time_string})
            
        response = gptbot(message)
        now = datetime.now()
        date_time_string = now.strftime("%m/%d/%Y %H:%M:%S")
        chat = Chat(user=request.user, message=message, response=response, created_at=date_time_string)
        chat.save()
        print(response)
        return JsonResponse({'message': message, 'response': response, 'created_at': date_time_string})
    return render(request, 'home.html', {'chats': chats})
    

# signup page
def user_signup(request):
    
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            
            address = form.cleaned_data['address']
            username = form.cleaned_data['username'] 
            user= User.objects.get(username=username) #user instance
            
            city_address = UserAddress(username=user, city=address)
            city_address.save()
            #print(city_address)
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
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
                form.add_error(None, 'Invalid username or password. Please try again.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')