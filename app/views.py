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
from chatbot.model.db_fetch import text_to_sql 
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
    # print(user.username)
    # print(user.id)
    location = UserAddress.objects.get(username_id=user.username)
    # print(location.city)
    keywords = ["list","how many", "address", "location", "procedures"]
    appointment_keywords = ["appointment","set an appointment", "set appointment"]
    procedure_list = ["Dental Cleanings", "Fillings", "Root Canal Therapy", "Tooth Extraction", "Crowns", "Bridges", "Dental Implants", "Dentures", "Teeth Whitening", "Dental Checkup"]
    if request.method == 'POST':
        message = request.POST.get('message')
        keywords_list = any(keyword in message for keyword in keywords)
        if keywords_list:
            """Sets appointment using series of questions. Returns sql INSERT statement."""
            response = text_to_sql(message)
            print(response)
            now = datetime.now()
            date_time_string = now.strftime("%m/%d/%Y %H:%M:%S")
            chat = Chat(user=request.user, message=message, response=response, created_at=date_time_string)
            chat.save()
            return JsonResponse({'message': message, 'response': response, 'created_at': date_time_string})

        appointment_keywords_list = any(keyword_appt in message for keyword_appt in appointment_keywords)
        if appointment_keywords_list:
            dentist_query = f"""SELECT clinic_code, dentist_name from app_dentist where city_town LIKE '%{location.city}%';"""
            
            conn = psycopg2.connect(user="johnnicholasmdato",
                                            password="JBmMq1Dsd3fn",
                                            host="ep-still-pine-74876349.ap-southeast-1.aws.neon.tech",
                                            port="5432",
                                            database="healthcare_dental")
            # conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password, sslmode=sslmode)
            cur = conn.cursor()
            cur.execute(dentist_query)
            dentist_select = str(cur.fetchall())

            response = f"""Please specify your appointment details in this format (dentist code, ppointment date(mm/dd/yyyy), time(24hr format), procedure type)\nHere's the list of nearby dentist based on your location:\n{dentist_select}"""
            # insert_appointment = message.split(",")
            # print(insert_appointment)
            now = datetime.now()
            date_time_string = now.strftime("%m/%d/%Y %H:%M:%S")
            chat = Chat(user=request.user, message=message, response=response, created_at=date_time_string)
            chat.save()
            return JsonResponse({'message': message, 'response': response, 'created_at': date_time_string})
        
        procedures_keywords_list = any(keyword_procedures in message for keyword_procedures in procedure_list)
        if procedures_keywords_list:
            insert_appointment = message.split(",")
            print(insert_appointment)
            sql_query = f"""SELECT clinic_id from app_dentist where clinic_code ILIKE '%{insert_appointment[0]}%';"""
            

        #     sql_query = f"""INSERT INTO app_dentist_schedule (clinic_id, "user_id", appointment_date, "start", stop, procedure_type, reference_number)
        # values ({clinic_id}, {user_id}, '{apt_date.strftime('%Y-%m-%d')}', {time_start}, {time_start + 1}, '{procedure}', '{ctrl_number}');"""

        #     print(f"""\nAPPOINTMENT SUMMARY for {ctrl_number}:
        # {procedure} at {clinic} on {apt_date.strftime('%m/%d/%Y')}, {time_start}:00 - {time_start + 1}:00""")
            
            # connect to db
            conn = psycopg2.connect(user="johnnicholasmdato",
                                            password="JBmMq1Dsd3fn",
                                            host="ep-still-pine-74876349.ap-southeast-1.aws.neon.tech",
                                            port="5432",
                                            database="healthcare_dental")
            # conn = psycopg2.connect(dbname=dbname, user=user, host=host, password=password, sslmode=sslmode)
            cur = conn.cursor()
            cur.execute(sql_query)
            clinic_id = str(cur.fetchone())
            clinic_id = clinic_id[1:5]
            print(clinic_id)
            clinic_name =  f"""SELECT clinic_name from app_dentist where clinic_id = '{clinic_id}';"""
            cur.execute(clinic_name)
            clinic_name = str(cur.fetchone())
            clinic_name = clinic_name[2:-3]
            print(clinic_name)
            ctrl_number = "QC" + str(insert_appointment[1].replace("/", "")) + str(clinic_id) + str(user.id)
            print(ctrl_number)
            insert_query = f"""INSERT INTO app_dentist_schedule (clinic_id, "user_id", appointment_date, "start", stop, procedure_type, reference_number)
        values ({clinic_id}, {user.id}, '{insert_appointment[1].strip()}', {int(insert_appointment[2].strip())}, {int(insert_appointment[2].strip()) + 1}, '{insert_appointment[3].strip()}', '{ctrl_number}');"""
            cur.execute(insert_query)
            conn.commit()
            cur.close()
            conn.close()
  
            response = f"""\nAPPOINTMENT SUMMARY\nReference Number: {ctrl_number.upper()} \nAppointment Details:{insert_appointment[3].strip()} at {clinic_name.strip()} on {insert_appointment[1].strip()} {int(insert_appointment[2].strip())}:00 - {int(insert_appointment[2].strip()) + 1}:00"""
            now = datetime.now()
            date_time_string = now.strftime("%m/%d/%Y %H:%M:%S")
            chat = Chat(user=request.user, message=message, response=response, created_at=date_time_string)
            chat.save()
            return JsonResponse({'message': message, 'response': response, 'created_at': date_time_string})

        # response = chain.predict(input=message)
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
