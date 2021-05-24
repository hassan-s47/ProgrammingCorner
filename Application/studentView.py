# write all functions related to student here\
from Application.views import CompilerForm
from .forms import CreateClassForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LabRoom,Teacher,CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
import random, string
from django.core.files.storage import FileSystemStorage
from .scrap import Scrapper
from .models import CustomUser, Student, LabRoom ,student_Class,Teacher, Assessment, Question, TestCase
from Application.EmailBackEnd import EmailBackEnd
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
# from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime
import json

# @ensure_csrf_cookie
class TempShow: # change class name
  
    def __init__(self,n,i,c,t,p):
        self.c_name=n
        self.id=i
        self.student_count=c
        self.teacher=t
        self.teacher_profie=p

def StudentDashboardPage(request):
    total_courses=student_Class.objects.filter(student_id=request.user)
    course_info=[]

    i=0
    for corse in total_courses:
        temp=student_Class.objects.filter(class_id=corse.class_id).count()
        Teacher_obbj=Teacher.objects.get(admin=corse.class_id.tutor)
        print(Teacher_obbj)
        obj=TempShow(corse.class_id.className,corse.class_id.id,temp,corse.class_id.tutor.username,Teacher_obbj)
        
        course_info.append(obj)
   
    student_obj=CustomUser.objects.get(id=request.user.id)
    student_obbj=Student.objects.get(admin=student_obj)
    
    course_count=total_courses.count()
   
    context = {'classes':total_courses,'total':course_count,'student_obj':student_obbj,'course_info':course_info}
    return(render(request, 'Application/studentDashboard.html',context))
def JoinClass(request):
    if request.method=="POST":
        class_obj=None
        classCode=request.POST.get("classCode")
        student_id=request.POST.get("student_id")
        try:
            std=Student()
            result=std.joinLabRoom(student_id,classCode)
            if result==True:
                messages.success(request, 'Class Joined Successfully')
                return HttpResponseRedirect(reverse("Studentdashboard"))
            else:
                messages.info(request, 'Class Code is Incorrect')
                return HttpResponseRedirect(reverse("Studentdashboard"))
        except:
            messages.info(request, 'Class Code is Incorrect')
            return HttpResponseRedirect(reverse("Studentdashboard"))
    
  
    else:
        return HttpResponseRedirect(reverse("Studentdashboard"))
def ChngeProfileView(request):
    if request.method=="POST":
        profile_pic=request.FILES['profile_pic']
        std_id=request.POST.get("std_id")
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        
        std=Student()
        std.changeProfile(std_id,profile_pic_url)
        return HttpResponseRedirect(reverse("Studentdashboard"))
    else:
        return HttpResponseRedirect(reverse("Studentdashboard"))
def ChangePasswordView(request):
    if request.method=="POST":
       
        password=request.POST.get("password")
        std=Student()
        std.changePassword(request.user.id,password)

        return HttpResponseRedirect(reverse("Studentdashboard"))
    else:
        return HttpResponseRedirect(reverse("Studentdashboard"))
    pass

def viewClassStudent(request,id):
    now = datetime.now()
    assessments=Assessment.objects.all().filter(course_id=id,due_date__gte = datetime.now())
    assessments_pa=Assessment.objects.all().filter(course_id=id,due_date__lt = datetime.now())
    assessments_count=Assessment.objects.all().filter(course_id=id).count()
    print(assessments_pa)
    students_obj=student_Class.objects.all().filter(class_id=id)
    no_of_student=len(students_obj)
    lab_obj=LabRoom.objects.get(id=id)
    return (render(request,'Application/courseStudent.html',{"assessments_count":assessments_count, "assessments_up":assessments,"count":no_of_student,"assessments_pa":assessments_pa,"labdetail":lab_obj,"students":students_obj}))


def viewAssessment(request):
    if request.method!="POST":
         #form is not submitted 
        assessment_id1 = request.GET.get("id")
        print(assessment_id1)
        items = Question.objects.all().filter(assessment_id=assessment_id1)
        print(items)
        return(render(request,'Application/viewAssessmentStd.html', {"items":items, "assessment_id":assessment_id1}))
    else:
        assessment_id1 = request.POST.get("id")
        print("Assessment ID",assessment_id1)
        statement = request.POST.get("statement")
        weightage = request.POST.get("weightage")
        postData=json.loads(request.POST.get('DataSend'))
        question=Question()
        assessment_obj = Assessment.objects.all().get(id=assessment_id1)
        question=question.addQuestion(assessment_obj, statement, weightage)
        for items in postData:
            input=items['input']
            output=items['output']
            testCase=TestCase()
            testCase.addTestCase(question, input, output)

        items = Question.objects.all().filter(assessment_id=assessment_id1)
        return(render(request,'Application/viewAssessmentStd.html', {"items":items, "assessment_id":assessment_id1}))

def attemptQuestion(request,id):
    return CompilerForm.as_view(template_name = "form.html")