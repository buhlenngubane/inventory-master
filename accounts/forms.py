from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Employee
from django import forms
from django_password_eye.fields import PasswordEye


class EmployeeCreationForm(UserCreationForm):
    password1 = PasswordEye(label='')
    password2 = PasswordEye(label='')
    class Meta(UserCreationForm):
        model = Employee
        fields=['first_name','last_name','username','email','password1','password2']


class CustomAuthenticationForm(AuthenticationForm):
    password = PasswordEye(label='')
    class Meta:
        model = Employee
        fields = ['username', 'password']

class CustomAuthenticationFormReset(PasswordResetForm):
    class Meta:
        model = Employee
        fields = ['Email']
