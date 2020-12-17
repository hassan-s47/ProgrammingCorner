# write all functions related to teacher here\
from .forms import CreateClassForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LabRoom,Teacher,CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
import random, string
from django.core.files.storage import FileSystemStorage
from .scrap import Scrapper
def createClass(request):
    
    if request.method=="POST":
        className=request.POST.get("className")
        
        tutor=request.user
        try:
            t=Teacher()
            t.createClass(className,tutor)
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
        t=Teacher()
        t.changeProfile(std_id,profile_pic_url)
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return HttpResponseRedirect(reverse("dashboard")) 
def dashboardPage(request):
    student_obj=CustomUser.objects.get(id=request.user.id)
    student_obbj=Teacher.objects.get(admin=student_obj)
    context = {'LabRoom' : LabRoom.objects.filter(tutor=request.user),'student_obj':student_obbj}
    return(render(request, 'Application/dashboard.html', context))
def ViewScrapper(request):
    context={}
    if request.method=="POST":
        topicname=request.POST.get("topic")
        print(topicname)
        
        sc = Scrapper()

        results = sc.getquestionlist("Loops")
        print(results)
        if results is not None:

            for i,res in enumerate(results):
                print (i,res.get_attribute ("innerText"),"\n\n")
                            
        sc.driver.quit()
        return(render(request, 'Application/scraperView.html', context))

   
    return(render(request, 'Application/scraperView.html', context))