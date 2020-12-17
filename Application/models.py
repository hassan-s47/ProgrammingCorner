
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

User._meta.get_field('email')._unique = True
class CustomUser(AbstractUser):
    user_type_data=((1,"Teacher"),(2,"Student"),(3,'Admin'))
    user_type=models.CharField(default=3,choices=user_type_data,max_length=10)

    def dologin(self,email_obj,username,password,request):

        user=email_obj.authenticate(request,username=request.POST.get("email"),password=request.POST.get("password"))
                
       

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

        class_obj= LabRoom.objects.get(classCode=classCode)
        if class_obj!=None:
            obj=student_Class(student_id=userid, class_id=class_obj)
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
        Class=LabRoom(className=className,tutor=userid, classCode=classCode)
        Class.save()
    def changeProfile(self,userid,new_url):
        tech=Teacher.objects.get(admin=userid)
        tech.profile_pic=new_url
        tech.save()


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




@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==2:

            Student.objects.create(admin=instance,rollNo="",profile_pic="http://placehold.it/263X263")
        if instance.user_type==1:
            Teacher.objects.create(admin=instance,profile_pic="http://placehold.it/263X263")
        # if instance.user_type==3:
        #     Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==2:
        instance.student.save()
    if instance.user_type==1:
        instance.teacher.save()
    # if instance.user_type==3:
    #     instance.students.save()  