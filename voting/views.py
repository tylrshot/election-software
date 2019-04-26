from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
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

def error(request):
    return render(request, 'voting/failed.html')

def submit(request, poll_id, user_id):
    user = request.user
    if user.id != user_id:
        return HttpResponseRedirect('responseError')
    
    if request.method == 'POST':
        submission = request.POST
    else:
        return HttpResponseRedirect('responseError')
    
    #{[question id, response 1], [question id, response 1, response 2]}
    responses = []
    for x in submission:
        if x != 'csrfmiddlewaretoken':
            currentResponse = [x]
            currentData = submission.getlist(x)
            
            #If the question has a submission with more than 1 response, checks if it is the correct number responses for the question
            print(currentData)
            currentLength = currentData.__len__()
            if currentLength > 0:
                maxLength = Question.objects.get(id=x).choicesAccepted
                print(maxLength)
                print(currentLength)
                if currentLength > maxLength:
                    return HttpResponseRedirect('/responseError')
                
            #Appends response in array
            for x in currentData:
                currentResponse.append(x)
                
            responses.append(currentResponse)
            
    print(responses)
            #print(x)
            #print(submission.get(x))
    
    #info = submission
    info = submission
    
    args = {'info':info}
    return render(request, 'voting/submit.html', args)

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

