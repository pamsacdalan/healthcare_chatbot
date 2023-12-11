from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_process, logout 
from .forms import UserCreationForm, LoginForm, SignupForm
from django.contrib import messages
from dotenv import load_dotenv


from django.http import JsonResponse
from .models import Chat, Dentist_Schedule, UserAddress,appointment_schedule
from datetime import datetime
from chatbot.local_history import chain
from chatbot.model.gptbot import gptbot
from chatbot.langsql.converted_functions.appointment import *

from psycopg2 import Error


import psycopg2
import pandas as pd
from datetime import datetime

from dotenv import dotenv_values


# loading the credentials
db_creds = dotenv_values("app\.env")
host = db_creds['HOST']
user = db_creds['USER']
password = db_creds['PASSWORD']
dbname = db_creds['DB']
sslmode=db_creds['SSLMODE']


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
        #response = chain.predict(input=message)
        response = gptbot(message)
        
        if "appointment" in response:
                # """Sets appointment using series of questions. Returns sql INSERT statement."""
            user_id = user.id
            city = location.city.upper()
            procedure = procedure_selector()
            print("\n")
            clinic_list, city = city_selector(city)
            print("\n")
            clinic = dentist_selector(clinic_list)
            print("\n")
            print(clinic)
            clinic_id = get_clinic_id(clinic, city)
            print("\n")
            apt_date = date_selector(clinic_id)
            print("\n")
            time_start = time_selector(apt_date, clinic_id)
            ctrl_number = generate_ctrl_num(apt_date)

            sql_query = f"""INSERT INTO app_dentist_schedule (clinic_id, "user_id", appointment_date, "start", stop, procedure_type, reference_number)
        values ({clinic_id}, {user_id}, '{apt_date.strftime('%Y-%m-%d')}', {time_start}, {time_start + 1}, '{procedure}', '{ctrl_number}');"""
    
            print(f"""\nAPPOINTMENT SUMMARY for {ctrl_number}:
        {procedure} at {clinic} on {apt_date.strftime('%m/%d/%Y')}, {time_start}:00 - {time_start + 1}:00""")
            
            # connect to db
            conn = psycopg2.connect(user="johnnicholasmdato",
                                            password="JBmMq1Dsd3fn",
                                            host="ep-still-pine-74876349.ap-southeast-1.aws.neon.tech",
                                            port="5432",
                                            database="healthcare_dental")
            # conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password, sslmode=sslmode)
            cur = conn.cursor()
            cur.execute(sql_query)

            conn.commit()
            cur.close()
            conn.close()
          
        #response = response[1:]
        now = datetime.now()
        date_time_string = now.strftime("%m/%d/%Y %H:%M:%S")
        chat = Chat(user=request.user, message=message, response=response, created_at=date_time_string)
        # appt = appointment_schedule(clinic_id = 1,user_id = 1,appointment_date= "2023-12-22", start = 9, stop = 10, procedure_type= "DENTAL CLEANINGS", reference_number = "Q23231432434")
        #print(date_time_string)
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
