from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path("signup/", views.signup, name='signup'),
    path("login/", views.LoginView.as_view(), name='login'),
    path("friends/", views.friends, name="friends"), 
]