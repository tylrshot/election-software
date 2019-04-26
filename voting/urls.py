from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('poll/<int:poll_id>/', views.poll, name='poll'),
    path('profile', views.profile, name='profile'),
    #path('login', views.login, name='login'),
]