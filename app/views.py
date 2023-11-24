from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as login_process, logout 
from .forms import UserCreationForm, LoginForm, SignupForm
from django.contrib import messages
#from chatbot.langsql.chat import conversation
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.llms import HuggingFaceHub
from langchain.chains.conversation.memory import ConversationBufferMemory

from django.http import JsonResponse
from .models import Chat
from django.utils import timezone

# Create your views here.

def login(request):
    return render(request, 'login.html')

def home(request):
    chats = Chat.objects.filter(user=request.user)

    load_dotenv()
    llm = HuggingFaceHub(repo_id='lmsys/fastchat-t5-3b-v1.0')
    memory = ConversationBufferMemory()
    
    conversation = ConversationChain(
    llm=llm,
    memory=memory,
    )
    
    if request.method == 'POST':
        message = request.POST.get('message')
        response = conversation.predict(input=message)
        response = response[5:]
        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({'message': message, 'response': response})
    return render(request, 'home.html', {'chats': chats})

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

