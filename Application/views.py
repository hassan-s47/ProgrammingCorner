from django.http import HttpResponse
from .models import CustomUser
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateStudentForm, CreateClassForm
from django.contrib import messages
from django.contrib.auth import  login, logout
from .models import Student
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import CustomUser, Student, Classroom ,student_Class,Teacher
from Application.EmailBackEnd import EmailBackEnd
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required


def homePage(request):
    context = {}
    return(render(request, 'Application/home.html', context))
    
def registerPage(request):
    
    form = CreateStudentForm()
    if request.method == 'POST':
        check = request.POST.get('customCheck')
        if(check == 'on'):
            form = CreateStudentForm(request.POST)
            if form.is_valid():
                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                rollNo=form.cleaned_data["rollNo"]
                try:
                    print("Here")
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name="default",first_name="default",user_type=2)
                    user.student.rollNo=rollNo
                    
                    print("Roll No :",user.student.rollNo)
                        
                    user.save()
                    return HttpResponseRedirect(reverse("login"))
                
                except:
                    messages.error(request,"Failed to Add Student")
                    return HttpResponseRedirect(reverse("register"))
                
                    
            else:

                form=CreateStudentForm(request.POST)
                return render(request, "Application/regsiter.html", {"form": form})        
        else:
            form = CreateStudentForm(request.POST)
            if form.is_valid():

                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                try:
                    print("Here")
                    user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name="default",first_name="default",user_type=1)
                    user.save()
                    messages.success(request,"Successfully Added Teacher",username)
                    return HttpResponseRedirect(reverse("login"))
                
                    
                
                except:
                    messages.error(request,"Failed to Add Teacher")
                    return HttpResponseRedirect(reverse("register"))
            else:

                form=CreateStudentForm(request.POST)
                return render(request, "Application/regsiter.html", {"form": form})     

               
    context = {'form' : form}
    return(render(request, 'Application/register.html', context))

def loginPage(request):
    context={}
    if request.method!="POST":
        return(render(request, 'Application/login.html', context))
    else:
        user=EmailBackEnd.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1": # if teacher redirect to teacher dashboard
                return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type=="2": # else to student
                return HttpResponseRedirect(reverse("Studentdashboard"))
            
        
            
        else:
            messages.info(request, 'Username OR Password is incorrect')
            return(render(request, 'Application/login.html', context))

    
def logoutUser(request):
    logout(request)
    return(redirect('login'))


