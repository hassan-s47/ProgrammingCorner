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
from .models import CustomUser, Student, LabRoom ,student_Class,Teacher, Assessment, Question, TestCase
from Application.EmailBackEnd import EmailBackEnd
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.edit import FormView
from .forms import SampleForm
from .compiler import Compiler
from .compiler import Compiler
import json



class CompilerForm(FormView):
    template_name = 'Application/form.html'
    form_class = SampleForm
    success_url = "/dashboard"
    studentID = ""
  

    def get_context_data(self,**kwargs):
        context = super(CompilerForm, self).get_context_data(**kwargs)
        print(self.studentID)
        context['id'] = self.kwargs.get('id')
        return context

   




def getResponse(request):
    data=request.POST.get("code")
    inp  = request.POST.get("input")
    print(data,inp)
    compiler=Compiler(data,inp)
    output=compiler.run(inp)
    return HttpResponse(json.dumps({'output' : output}), content_type='application/json')


def homePage(request):
   
    return (render(request, 'Application/home.html'))
    
def RegisterPage(request):
    
    
    if request.method == 'POST':
        check = request.POST.get('customCheck')
        if(check == 'on'):
            form = CreateStudentForm(request.POST)
            if form.is_valid():   # if all input feilds are filled
                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                rollNo=form.cleaned_data["rollNo"]
                try:
                    print("Here")
                    std=Student()
                    std.register(username,password,email,rollNo)
                    messages.success(request,"Student Registration Successfully")
                    return HttpResponseRedirect(reverse("login"))
                
                except:
                    messages.error(request,"Failed to Add Student")
                    return HttpResponseRedirect(reverse("register"))
                
                    
            else: # if feilds are not filled/or any condition wrong

                form=CreateStudentForm(request.POST)
                return render(request, "Application/regsiter.html", {"form": form})        
        else:
            # post request and checkbox not on 
            form = CreateStudentForm(request.POST)
            if form.is_valid():

                username=form.cleaned_data["username"]
                email=form.cleaned_data["email"]
                password=form.cleaned_data["password"]
                try:
                    t=Teacher()
                    t.register(username,email,password) 
                    messages.success(request,"Successfully Added Teacher",username)
                    return HttpResponseRedirect(reverse("login"))
                
                    
                
                except:
                    messages.error(request,"Failed to Add Teacher")
                    return HttpResponseRedirect(reverse("register"))
            else:

                form=CreateStudentForm(request.POST)
                return render(request, "Application/regsiter.html", {"form": form})     

    form = CreateStudentForm()          
    context = {'form' : form}
    return(render(request, 'Application/register.html', context))

def LoginPage(request):
    context={}
    if request.method!="POST": #form is not submitted 
        return(render(request, 'Application/login.html', context)) # show page only
    else:
        email=request.POST.get("email")
        passwords=request.POST.get("password")
        obj=CustomUser()
        user=obj.dologin(EmailBackEnd,email,passwords,request)
        if user!=None:
            login(request,user)
            if user.user_type=="1": # if teacher redirect to teacher dashboard
                return HttpResponseRedirect(reverse("dashboard"))
            elif user.user_type=="2": # else to student
                return HttpResponseRedirect(reverse("Studentdashboard"))
            
        
            
        else:
            #worong email/Password
            messages.info(request, 'Login Failed. Email OR Password is incorrect')
            return(render(request, 'Application/login.html', context))

    
  # common functions for both teacher and Student   
def LogoutUser(request):
    logout(request) #django builtin logout function
    return(redirect('login'))

def courseDetails(request):
    return(render(request,'Application/course.html'))

def courseDetailsStudent(request):
    return(render(request, 'Application/courseStudent.html'))
    
def viewAssessment(request):
    #get assessment from that teacher and display here
    
    return(render(request,'Application/manageAssessments.html'))

def manaegQuestions(request):
   
    return(render(request,'Application/addQuestion.html'))


