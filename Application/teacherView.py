# write all functions related to teacher here\
from .forms import CreateClassForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LabRoom, Teacher, CustomUser
from django.shortcuts import render, redirect
from django.contrib import messages
import random
import string
from django.core.files.storage import FileSystemStorage
from .scrap import Scrapper
from .models import CustomUser, Marks, Student, LabRoom, student_Class, Teacher, Assessment, Question, TestCase
from Application.EmailBackEnd import EmailBackEnd
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from datetime import datetime
import json


@ensure_csrf_cookie
def CreateClass(request):

    if request.method == "POST":
        className = request.POST.get("className")
        tutor = request.user
        t = Teacher()
        s = t.createClass(className, tutor)
        messages.success(
            request, "Successfully Added Class With Class Code : " + s)
        return HttpResponseRedirect(reverse("dashboard"))

    else:
        return HttpResponseRedirect(reverse("dashboard"))


def TeacherChngeProfile(request):
    if request.method == "POST":

        profile_pic = request.FILES['profile_pic']
        std_id = request.POST.get("std_id")
        fs = FileSystemStorage()
        filename = fs.save(profile_pic.name, profile_pic)
        profile_pic_url = fs.url(filename)
        t = Teacher()
        t.changeProfile(std_id, profile_pic_url)
        return HttpResponseRedirect(reverse("dashboard"))

    else:
        return HttpResponseRedirect(reverse("dashboard"))


def DashboardPage(request):
    student_obj = CustomUser.objects.get(id=request.user.id)
    student_obbj = Teacher.objects.get(admin=student_obj)
    context = {'Classroom': LabRoom.objects.filter(
        tutor=request.user), 'student_obj': student_obbj}
    return(render(request, 'Application/dashboard.html', context))


def RemoveClass(request, id):
    t = Teacher()
    t.removeLab(id)
    return HttpResponseRedirect(reverse("dashboard"))


def ViewScrapper(request):
    context = {}

    if request.method == "POST":
        topicname = request.POST.get("topic")
        assessment_id = request.POST.get("assessment_id")
        print(topicname)

        sc = Scrapper()

        results = sc.getquestionlist(topicname)
        questionlist = []
        if results is not None:

            for res in results:
                questionlist.append(res.get_attribute("innerText"))

        sc.driver.quit()
        context = {'questionlist': questionlist,
            "assessment_id": assessment_id}
        return(render(request, 'Application/scraperView.html', context))

    return(render(request, 'Application/scraperView.html', context))


def createAssessment(request):
    items = LabRoom.objects.all().filter(tutor=request.user.id)
    if request.method != "POST":  # form is not submitted
        # show page only
        return(render(request, 'Application/createAssignment.html', {"items": items}))
    else:
        courseId = request.POST.get("courseId")
        name = request.POST.get("title")
        startDate = request.POST.get("startDate")
        dueDate = request.POST.get("dueDate")
        description = request.POST.get("description")
        assessment = Assessment()
        assessment_id = assessment.addAssessment(
            courseId, name, startDate, dueDate, description)
        items = Question.objects.all().filter(assessment_id=assessment_id)
        # return(render(request,'Application/addQuestion.html', {"courseId":courseId, "items":items, "assessment":assessment}))
        return redirect('/addQuestion?id=' + str(assessment_id))


def addQuestion(request):
    print("EELO")

    if request.method != "POST":
        #form is not submitted
        assessment_id1 = request.GET.get("id")
        print(assessment_id1)
        items = Question.objects.all().filter(assessment_id=assessment_id1)
        print(items)
        return(render(request, 'Application/addQuestion.html', {"items": items, "assessment_id": assessment_id1}))
    else:
        assessment_id1 = request.POST.get("id")
        print("Assessment ID", assessment_id1)
        statement = request.POST.get("statement")
        weightage = request.POST.get("weightage")
        postData = json.loads(request.POST.get('DataSend'))
        question = Question()
        assessment_obj = Assessment.objects.all().get(id=assessment_id1)
        question = question.addQuestion(assessment_obj, statement, weightage)
        for items in postData:
            input = items['input']
            output = items['output']
            testCase = TestCase()
            testCase.addTestCase(question, input, output)

        items = Question.objects.all().filter(assessment_id=assessment_id1)
        return(render(request, 'Application/addQuestion.html', {"items": items, "assessment_id": assessment_id1}))


def RemoveQuestion(request, id):
    print(request)
    q = Question()
    q.removeQuestion(id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def updateQuestion(request):

    assessment_id1 = request.POST.get("id")
    print("qUESTION ID", assessment_id1)
    statement = request.POST.get("statement")
    weightage = request.POST.get("weightage")
    postData = json.loads(request.POST.get('DataSend'))
    question = Question()
    #
    question.editQuestion(assessment_id1, statement, weightage)
    testCase = TestCase()
    testCase.deleteTestCase(assessment_id1)
    question = Question.objects.all().get(id=assessment_id1)
    for items in postData:
        input = items['input']
        output = items['output']

        testCase.addTestCase(question, input, output)

    items = Question.objects.all().filter(assessment_id=assessment_id1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def editQuestion(request, id):
    if id != None:
        if request.method != "POST":
            item = Question.objects.get(id=id)
            testcases = TestCase.objects.all().filter(question_id=id)
            print(testcases)
            return (render(request, 'Application/editQuestion.html', {"Question": item, "TestCase": testcases, "question_id": id}))
        else:
            return redirect('/dashboard/')

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def updateAssessment(request):
    courseId = request.POST.get("courseId")
    ass_id = request.POST.get("assessment_id")
    name = request.POST.get("title")
    startDate = request.POST.get("startDate")
    dueDate = request.POST.get("dueDate")
    description = request.POST.get("description")
    assessment = Assessment()
    assessment_id = assessment.updateAssessment(
        ass_id, courseId, name, startDate, dueDate, description)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def editAssessment(request, id):
    lab = LabRoom.objects.all().filter(tutor=request.user.id)
    if id != None:
        if request.method != "POST":
            item = Assessment.objects.get(id=id)
            return (render(request, 'Application/editAssessment.html', {"Assessment": item, "assessment_id": id, "items": lab}))
        else:
            return redirect('/dashboard/')

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def viewClass(request, id):
    now = datetime.now()
    total_assessment = Assessment.objects.all().filter(course_id= id)
    assessments = Assessment.objects.all().filter(
        course_id=id, due_date__gte=datetime.now())
    assessments_pa = Assessment.objects.all().filter(
        course_id=id, due_date__lt=datetime.now())
    assessments_count = Assessment.objects.all().filter(course_id=id).count()
    students_obj = student_Class.objects.all().filter(class_id=id)
    no_of_student = len(students_obj)
    lab_obj = LabRoom.objects.get(id=id)
    return (render(request, 'Application/course.html', {"total_assessment":total_assessment,"assessments_count": assessments_count, "assessments_up": assessments, "count": no_of_student, "assessments_pa": assessments_pa, "labdetail": lab_obj, "students": students_obj}))


def viewAssessment(request):
    if request.method != "POST":
        #form is not submitted
        assessment_id1 = request.GET.get("id")
        print(assessment_id1)
        items = Question.objects.all().filter(assessment_id=assessment_id1)
        print(items)
        return(render(request, 'Application/viewAssessment.html', {"items": items, "assessment_id": assessment_id1}))
    else:
        assessment_id1 = request.POST.get("id")
        print("Assessment ID", assessment_id1)
        statement = request.POST.get("statement")
        weightage = request.POST.get("weightage")
        postData = json.loads(request.POST.get('DataSend'))
        question = Question()
        assessment_obj = Assessment.objects.all().get(id=assessment_id1)
        question = question.addQuestion(assessment_obj, statement, weightage)
        for items in postData:
            input = items['input']
            output = items['output']
            testCase = TestCase()
            testCase.addTestCase(question, input, output)

        items = Question.objects.all().filter(assessment_id=assessment_id1)
        return(render(request, 'Application/viewAssessment.html', {"items": items, "assessment_id": assessment_id1}))


def deleteAssessment(request, id):

    assessment = Assessment.objects.get(pk=id)
    assessment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class Result:
    def __init__(self,name,marklist,marks):
        self.name = name
        self.marklist = marklist
        self.totalmarks = marks


def viewResult(request,id):
    assessment = Assessment.objects.get(pk=id) #get the assessment
    course = LabRoom.objects.get(id=assessment.course_id) #get the course
    students = student_Class.objects.all().filter(class_id = course.id) #get the students
    questions = Question.objects.all().filter(assessment_id=assessment.id) #get the questions
    totalMarks = 0
    for question in questions:
        totalMarks += question.weightage
    resultList = []
    for student in students:
        studentMarks = 0
        marklist = []
        for question in questions:
            marks = Marks.objects.get(questionID=question.id, student_id=student.id) #get the marks4
            marklist.append(marks.obtainedMarks)
            studentMarks += marks.obtainedMarks
        studentInfo = Student.objects.get(id=student.id)
        resultList.append(Result(studentInfo.rollNo,marklist,studentMarks))
    
    
    return(render(request, 'Application/viewResult.html', {"totalMarks": totalMarks, "resultList": resultList,"questionList":questions}))

