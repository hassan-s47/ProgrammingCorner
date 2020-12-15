# write all functions related to teacher here\
from .forms import CreateClassForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Classroom,Teacher,CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
import random, string
from django.core.files.storage import FileSystemStorage
from .scrap import Scrapper
def createClass(request):
    
    if request.method=="POST":
        className=request.POST.get("className")
        classCode=''.join(random.choices(string.ascii_letters + string.digits, k=6))
        tutor=request.user
        try:
            Class=Classroom(className=className,tutor=tutor, classCode=classCode)
            Class.save()
            messages.success(request,"Successfully Added Class With Class Code : " + classCode)
            return HttpResponseRedirect(reverse("dashboard"))
        except:
            messages.error(request,"Failed to Add Class")
            return HttpResponseRedirect(reverse("dashboard"))

    else:
        return HttpResponseRedirect(reverse("dashboard"))
def TchngeProfile(request):
    if request.method=="POST":
        profile_pic=request.FILES['profile_pic']
        std_id=request.POST.get("std_id")
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        print( profile_pic_url)
        student=Teacher.objects.get(admin=std_id)
        student.profile_pic=profile_pic_url
        student.save()
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return HttpResponseRedirect(reverse("dashboard")) 
def dashboardPage(request):
    student_obj=CustomUser.objects.get(id=request.user.id)
    student_obbj=Teacher.objects.get(admin=student_obj)
    context = {'Classroom' : Classroom.objects.filter(tutor=request.user),'student_obj':student_obbj}
    return(render(request, 'Application/dashboard.html', context))
def ViewScrapper(request):
    context={}
    if request.method=="POST":
        topicname=request.POST.get("topic")
        print(topicname)
        
        sc = Scrapper()

        results = sc.getquestionlist(topicname)
        questionlist = []
        if results is not None:

            for res in results:
                questionlist.append(res.get_attribute ("innerText"))

        context = {'questionlist': questionlist}             
        sc.driver.quit()
        return(render(request, 'Application/scraperView.html', context))

   
    return(render(request, 'Application/scraperView.html', context))