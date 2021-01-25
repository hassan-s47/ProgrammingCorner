from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):
    pass

    def process_view(self,request,view_func,view_args,view_kwargs):
        pass
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1": #means teacher
                if modulename == "Application.teacherView":
                    pass
                elif modulename == "Application.views" or modulename=='django.views.static' or modulename=='Application.scrap':
                    pass 
                else:
                    return HttpResponseRedirect(reverse('dashboard'))
            elif user.user_type == "2":
                if modulename == "Application.studentView":
                    pass
                elif modulename == "Application.views" or modulename=='django.views.static' :
                    pass
                else:
                    return HttpResponseRedirect(reverse("Studentdashboard"))  
        else:
            if request.path == reverse("login") or modulename == "Application.views"  :
                pass
            else:
                return HttpResponseRedirect(reverse('login'))            
    
          