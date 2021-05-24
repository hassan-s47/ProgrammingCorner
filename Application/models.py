
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import random, string
User._meta.get_field('email')._unique = True
class CustomUser(AbstractUser):
    user_type_data=((1,"Teacher"),(2,"Student"),(3,'Admin'))
    user_type=models.CharField(default=3,choices=user_type_data,max_length=10)

    def dologin(self,email_obj,username,password,request):
        #we have use AbstractUSer of django and builtin function ling authentication and for maintaining sessions 
        #so thats why we are using EmailBackend as middleware for authenticating User
        user=email_obj.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
                
       #emal baackend will return a user object if successfully login otherwise None

        return user
    def changePassword(self,userid):
        pass
    


class Student(models.Model):
    
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    rollNo = models.CharField(max_length=200, default='00F-0000',unique=True)
    profile_pic=models.FileField(default='http://placehold.it/263X263')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    def __str__(self):
        return 'Person(name='+self.rollNo+', age='+str(self.profile_pic)+ ')'
    def register(self,username,password,email,rollNo):
        user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name="default",first_name="default",user_type=2)
        user.student.rollNo=rollNo
        print("Roll No :",user.student.rollNo)      
        user.save()

    def changePassword(self,userid,password):
        student_obj=CustomUser.objects.get(id=userid)
        password2 = make_password(password)
        student_obj.password=password2  
        student_obj.save()   

    def changeProfile(self,userid,new_url):
        student=Student.objects.get(admin=userid)
        student.profile_pic=new_url
        student.save()

    def joinLabRoom(self,userid,classCode):
        student_obj=CustomUser.objects.get(id=userid)
        class_obj= LabRoom.objects.get(classCode=classCode)
        if class_obj!=None:
            obj=student_Class(student_id=student_obj, class_id=class_obj)
            obj.save()
            return True
        else:
            return False

class Teacher(models.Model):
   
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_pic=models.FileField(default='http://placehold.it/263X263')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    objects=models.Manager()
    def register(self,username,email,password):
        user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name="default",first_name="default",user_type=1)
        user.save()

    def createClass(self,className,userid):
        classCode=''.join(random.choices(string.ascii_letters + string.digits, k=6))
        print(classCode)
        Class=LabRoom(className=className,tutor=userid, classCode=classCode)
        Class.save()
        return classCode

    def changeProfile(self,userid,new_url):
        tech=Teacher.objects.get(admin=userid)
        tech.profile_pic=new_url
        tech.save()

    def removeLab(self,id):
        clas = LabRoom.objects.get(pk=id)
        clas.delete()
        

class LabRoom(models.Model):
    id = models.AutoField(primary_key=True)
    className = models.CharField(max_length=200)
    tutor = models.ForeignKey(CustomUser, default = None, on_delete=models.CASCADE)
    classCode = models.CharField(max_length=10,unique=True)
    objects=models.Manager()

class student_Class(models.Model):  
    id = models.AutoField(primary_key=True)
    student_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class_id=models.ForeignKey(LabRoom,  on_delete=models.CASCADE)

class Assessment(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.IntegerField(null=False)
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    description = models.CharField(max_length=200)
    def __str__(self):
        return self.name + " " + str(self.id)

    def addAssessment(self, courseid, name, startDate, dueDate, description):
        assessment = Assessment()
        assessment = Assessment(course_id=courseid, name=name, start_date=startDate, due_date=dueDate, description=description)
        assessment.save()
        return assessment.id
    def updateAssessment(self,ass_id,course_id,name, startDate, dueDate, description):
        obj=Assessment.objects.get(id=ass_id)
        obj.course_id=course_id
        obj.name=name
        obj.start_date=startDate
        obj.due_date=dueDate
        obj.description=description
        obj.save()


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    assessment_id = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    statement = models.CharField(max_length=200)
    weightage = models.IntegerField(null=False)

    

    def addQuestion(self, assessment_id, statement, weightage):
        question=Question()
        question=Question(assessment_id=assessment_id, statement=statement, weightage=weightage)
        question.save()
        return question
    def editQuestion(self, Question_id, statement,weightage):

        question_obj=Question.objects.get(id=Question_id)
        question_obj.statement=statement
        question_obj.weightage=weightage
        question_obj.save()
        return True

    def removeQuestion(self, question_id):
        clas = Question.objects.get(pk=question_id)
        clas.delete()
   

class TestCase(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    input_String = models.CharField(max_length=200)
    output_String = models.CharField(max_length=200)

    def addTestCase(self, question_id, input, output):
        testCase=TestCase()
        testCase=TestCase(question_id=question_id, input_String=input, output_String=output)
        testCase.save()
    def deleteTestCase(self,question_id):
        try:
            cases=TestCase.objects.get(question_id=question_id)
            if cases!=None:
                cases.delete()
        except:
            return





@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==2:
            Student.objects.create(admin=instance,rollNo="",profile_pic="http://placehold.it/263X263")
        if instance.user_type==1:
            Teacher.objects.create(admin=instance,profile_pic="http://placehold.it/263X263")
       
@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==2:
        instance.student.save()
    if instance.user_type==1:
        instance.teacher.save()
   