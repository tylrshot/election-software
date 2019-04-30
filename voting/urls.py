from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('responseError', views.error, name='error'),
    
    path('createUsers_tz27q5bQz/<str:key>', views.importUsers, name='importUsers'),
    
    path('electionAdmin', views.electionAdmin, name='electionAdmin'),
    path('electionAdmin/poll/<int:poll_id>', views.electionAdminResults, name='electionAdminResults'),
    
    path('poll/<int:poll_id>/submit/<int:maxChoicesAccepted>', views.submit, name='submit'),
    path('poll/<int:poll_id>/', views.poll, name='poll'),
    path('profile', views.profile, name='profile'),
    #path('login', views.login, name='login'),
]