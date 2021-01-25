from django.urls import path, include
from django.conf.urls.static import static
from . import views, teacherView,studentView
from ProgrammingCorner import settings
urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.RegisterPage, name='register'),
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
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)