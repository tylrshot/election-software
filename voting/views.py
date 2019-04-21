from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .models import Greeting

import requests
import os

# Create your views here.
def index(request):
    
    return render(request, 'voting/index.html')

def profile(request):
    
    return render(request, 'voting/profile.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
