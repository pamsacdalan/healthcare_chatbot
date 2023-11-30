from django import forms
from django.forms import Form, EmailField, CharField
from django.forms.widgets import PasswordInput, TextInput, EmailInput 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    first_name = CharField(max_length=100,
                                 required=True,
                                 widget=TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = CharField(max_length=100,
                                required=True,
                                widget=TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = CharField(max_length=100,
                               required=True,
                               widget=TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    address = CharField(max_length=100,
                               required=True,
                               widget=TextInput(attrs={'placeholder': 'Province',
                                                             'class': 'form-control',
                                                             }))
    email = EmailField(required=True,
                             widget=EmailInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    password1 = CharField(max_length=50,
                                required=True,
                                widget=PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = CharField(max_length=50,
                                required=True,
                                widget=PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'address','email', 'password1', 'password2']
        
    

class LoginForm(Form):
    username = CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    password = CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))

