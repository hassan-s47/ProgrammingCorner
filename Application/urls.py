from django.urls import path, include
from django.conf.urls.static import static
from . import views, teacherView,studentView
from django.views.generic.base import TemplateView
from ProgrammingCorner import settings
from .views import BasicSampleFormView
from django.conf.urls import include, url

urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.RegisterPage, name='register'),
    path('course/', views.courseDetails, name='course'),
    path('createAssessment/', teacherView.createAssessment, name='createAssessment'),
     path('updateAssessment/', teacherView.updateAssessment, name='updateAssessment'),
    path('teacherAssessments/', views.viewAssessment, name='viewAssessment'),
     path('addQuestion/', teacherView.addQuestion, name='addQuestion'),
    path('manaegQuestions/', views.manaegQuestions, name='manaegQuestions'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutUser, name='logout'),
    path('dashboard/', teacherView.DashboardPage, name='dashboard'),
    path('logout_user', views.LogoutUser,name="logout"),
    path('createClass',teacherView.CreateClass,name="createClass"),
    path('Studentdashboard/',studentView.StudentDashboardPage,name="Studentdashboard"),
    path('joinClass',studentView.JoinClass,name="joinClass"),
    path('chngeProfile',studentView.ChngeProfileView,name="chngeProfile"),
    path('changePassword',studentView.ChangePasswordView,name="changePassword"),
    path('TchngeProfile',teacherView.TeacherChngeProfile,name="TchngeProfile"),
    path('ViewScrapper/',teacherView.ViewScrapper,name="ViewScrapper"),
    path('delete/<int:id>/',teacherView.RemoveClass,name='delete_class'),
    path('viewClass/<int:id>/',teacherView.viewClass,name='view_class'),
    path('deleteQuestion/<int:id>/',teacherView.RemoveQuestion,name='delete_question'),
    path('editQuestion/<int:id>/',teacherView.editQuestion,name='edit_question'),

    path('editAssessment/<int:id>/',teacherView.editAssessment,name='edit_assessment'),
    
     path('updateQuestion/',teacherView.updateQuestion,name='update_question'),
     path('form/', BasicSampleFormView.as_view(template_name="Application/form.html"), name='codemirror-form'),
    path('response/',views.getResponse, name='response'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)