from django.urls import path, include
from django.conf.urls.static import static
from . import views, teacherView,studentView
from ProgrammingCorner import settings
urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', teacherView.dashboardPage, name='dashboard'),
    path('logout_user', views.logoutUser,name="logout"),
    path('createClass',teacherView.createClass,name="createClass"),
    path('Studentdashboard/',studentView.StudentdashboardPage,name="Studentdashboard"),
    path('joinClass',studentView.joinClass,name="joinClass"),
    path('chngeProfile',studentView.chngeProfile,name="chngeProfile"),
    path('changePassword',studentView.changePassword,name="changePassword"),
    path('TchngeProfile',teacherView.TchngeProfile,name="TchngeProfile"),
    path('ViewScrapper/',teacherView.ViewScrapper,name="ViewScrapper")
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)