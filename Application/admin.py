from django.contrib import admin

from .models import Student
from django.contrib.auth.admin import UserAdmin

from Application.models import CustomUser


class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser,UserModel)
admin.site.register(Student)

