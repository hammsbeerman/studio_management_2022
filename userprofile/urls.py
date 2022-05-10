from django.urls import path
from . import views

#app_name='userprofile'
urlpatterns = [
    #path('', views.home, name="home"),
    path('login_user', views.login_user, name='login'),
    path('logout_user', views.logout_user, name='logout'),
    path('register', views.register_user, name='register')
]