from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Student, Teacher, LabRoom

class CreateStudentForm(forms.Form):
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control",'placeholder':'example@email.com'}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control",'placeholder':'Enter password'}))
    rollNo=forms.CharField(label="Roll no.",max_length=50,required=False,widget=forms.TextInput(attrs={"class":"form-control",'placeholder':'XXF-XXXX'}))
    
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control",'placeholder':'Jon Doe'}))
      
        
class CreateClassForm(forms.Form):
    name=forms.CharField(label="Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    classCode=forms.CharField(label="Class Code", max_length=10, widget=forms.TextInput(attrs={"class":"form-control"}))
    
# class CreateTeacherForm(UserCreationForm):
#     class Meta:
#         model = Teacher
#         fields = ['username', 'email', 'password', 'password2']