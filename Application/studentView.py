# write all functions related to student here\
from .forms import CreateClassForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Classroom,student_Class,CustomUser,Student,Teacher
from django.shortcuts import render, redirect
from django.contrib import messages
import random, string
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password

def StudentdashboardPage(request):
    total_courses=student_Class.objects.filter(student_id=request.user)
    course_info={}
    i='0';
    for corse in total_courses:
        
        course_info[corse.class_id.className]={}
        
        temp=student_Class.objects.filter(class_id=corse.class_id).count()
        course_info[corse.class_id.className]['course_id']=corse.class_id.id
        course_info[corse.class_id.className]['name']=corse.class_id.className
        course_info[corse.class_id.className]['student_count']=temp
        course_info[corse.class_id.className]['teacher']=corse.class_id.tutor.username
        
        Teacher_obbj=Teacher.objects.get(admin=corse.class_id.tutor)
        course_info[corse.class_id.className]['teacher_profile']=Teacher_obbj
        
        # for key,value in course_info.items():
            
        #     for key2,value2 in value.items():
        #         print (key2,value2)
                
        
    
    
  
    student_obj=CustomUser.objects.get(id=request.user.id)
    student_obbj=Student.objects.get(admin=student_obj)
    
    course_count=total_courses.count()
   
    context = {'classes':total_courses,'total':course_count,'student_obj':student_obbj,'course_info':course_info}
    return(render(request, 'Application/studentDashboard.html',context))
def joinClass(request):
    if request.method=="POST":
        class_obj=None
        classCode=request.POST.get("classCode")
        student_id=request.POST.get("student_id")
        try:
            class_obj= Classroom.objects.get(classCode=classCode)
            if class_obj!=None:
                obj=student_Class(student_id=request.user, class_id=class_obj)
                obj.save()

                return HttpResponseRedirect(reverse("Studentdashboard"))
        except:
            messages.info(request, 'Class Code is Incorrect')

            return HttpResponseRedirect(reverse("Studentdashboard"))

        
        
        
       
        
    else:
        return HttpResponseRedirect(reverse("Studentdashboard"))
def chngeProfile(request):
    if request.method=="POST":
        profile_pic=request.FILES['profile_pic']
        std_id=request.POST.get("std_id")
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        print( profile_pic_url)
        student=Student.objects.get(admin=std_id)
        student.profile_pic=profile_pic_url
        student.save()
        return HttpResponseRedirect(reverse("Studentdashboard"))
    else:
        return HttpResponseRedirect(reverse("Studentdashboard"))
def changePassword(request):
    if request.method=="POST":
       
        password=request.POST.get("password")
        student_obj=CustomUser.objects.get(id=request.user.id)
        password2 = make_password(password)
        student_obj.password=password2
        
        student_obj.save()
        return HttpResponseRedirect(reverse("Studentdashboard"))
    else:
        return HttpResponseRedirect(reverse("Studentdashboard"))
    pass
