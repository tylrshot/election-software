from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('success', views.success, name='success'),
    
    path('responseError', views.error, name='error'),
    
    path('createUsers_tz27q5bQz/<str:key>/<int:sheetNumber>', views.importUsers, name='importUsers'),
    path('newUser', views.newUser, name='newUser'),
    path('createNewUser', views.createNewUser, name='createNewUser'),
    
    path('electionAdmin', views.electionAdmin, name='electionAdmin'),
    path('electionAdmin/poll/<int:poll_id>', views.electionAdminResults, name='electionAdminResults'),
    
    path('poll/<int:poll_id>/submit/<int:maxChoicesAccepted>', views.submit, name='submit'),
    path('poll/<int:poll_id>/', views.poll, name='poll'),
    path('profile', views.profile, name='profile'),
    #path('login', views.login, name='login'),
]