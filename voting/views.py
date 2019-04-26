from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .models import User, UserInfo, Poll, Question, Group, Student, Choice

#from .forms import PollForm

import requests
import os
import datetime

# Create your views here.
def index(request):
    
    return render(request, 'voting/index.html')

def profile(request):
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.filter(user=user)
    
    #Determines user grade/group
    grade = userInfo[0].gradeLevel
    gradeString = str(grade)
    group = Group.objects.filter(name=gradeString)
    
    #Gets current time to see if poll is active
    currentTime = datetime.datetime.now()
    
    #polls = Poll.objects.filter(groupsAllowed=group[0], active=True)
    polls = Poll.objects.filter(groupsAllowed=group[0], active=True, startTime__lte=currentTime, endTime__gte=currentTime)
    
    '''
    #Collects user's title
    title = userInfo[0].title
    userIsEditor = False
    if userTitle == 'L5':
        userIsEditor = True

    #Collects user's name
    firstName = userInfo[0].firstName
    lastName = userInfo[0].lastName


    #Collects user's pages
    userID = userInfo[0].id
    userPages = Page.objects.filter(assigned__id=userID)

    #Collects Deadlines
    deadlines = Deadline.objects.all()

    print(deadlines[0])
    '''
    
    args = {'user':user, 'grade':grade, 'polls':polls}

    return render(request, 'voting/profile.html', args)

def poll(request, poll_id):
    user = request.user

    #Gets extra info on user
    userInfo = UserInfo.objects.filter(user=user)

    try:
        thisPoll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Ballot does not exist")
        
    pollName = thisPoll.name
        
    questions = Question.objects.filter(poll=thisPoll).order_by('questionOrder')
    
    '''
    numQuestions = range(len(questions))
    
    questionsAndChoices = []
    for x in questions:
        choices = Choice.objects.filter(question=x)
        questionsAndChoices.append(choices)
        
    newQuestionsAndChoices = []
    for x in questions:
        choices = Choice.objects.filter(question=x)
        questionName = x.name
        tempQuestion = [questionName]
        for x in choices:
            choiceName = x.name
            tempQuestion.append(choiceName)
        newQuestionsAndChoices.append(tempQuestion)
        
    '''
        
    args = {'pollName':pollName, 'user':user, 'questions': questions}
    return render(request, 'voting/poll.html', args)

