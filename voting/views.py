from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone

import os

import collections

import csv

from .models import User, UserInfo, Poll, Question, Group, Response

#from .forms import PollForm

import requests
import os
import datetime


# Create your views here.
def index(request):
    
    return render(request, 'voting/index.html')

def success(request):
    
    return render(request, 'voting/success.html')

def newUser(request):
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    userIsAdmin = False
    if userInfo.admin == True:
        userIsAdmin = True
        
    if userIsAdmin == False:
        return HttpResponseRedirect('/profile')
    
    message = 'Nothing to show.'
    
    args = {'userIsAdmin':userIsAdmin, 'message':message}
    
    return render(request, 'voting/newUser.html', args)

def createNewUser(request):
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    userIsAdmin = False
    if userInfo.admin == True:
        userIsAdmin = True
        
    if userIsAdmin == False:
        return HttpResponseRedirect('/profile')
    
    if request.method == 'POST':
        submission = request.POST
    else:
        return HttpResponseRedirect('/responseError')
    
    newUser = User.objects.create_user(submission['GTID'], 'student@lumpkinschools.com', submission['LastName'])
    newUser.save()
    newUserInfo = UserInfo.objects.get(user=newUser)
    newUserInfo.gradeLevel = submission['Grade']
    newUserInfo.votedIN = [0]
    newUserInfo.save()
    
    message = 'New user created: ' + submission['GTID'] + ' with password ' + submission['LastName'] + ' and grade ' + submission['Grade']
    
    args = {'userIsAdmin':userIsAdmin, 'message':message}
    
    return render(request, 'voting/newUser.html', args)

def importUsers(request, key, sheetNumber):
    
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    userIsAdmin = False
    if userInfo.admin == True and key == "xAd6u2I":
        
        #allUsers = User.objects.filter(is_staff=False)
        #allUsers.delete()
        
        with open('voting/static/Sheet' + str(sheetNumber) + '.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            #Skips first line
            next(csv_reader)
            for line in csv_reader:
                user = User.objects.create_user(line[0], line[3], line[1])
                user.save()
                userInfo = UserInfo.objects.get(user=user)
                userInfo.gradeLevel = line[2]
                userInfo.votedIN = [0]
                userInfo.save()
        
        return HttpResponseRedirect('/profile')
        
    else:
    
        return render(request, 'voting/failed.html')

def electionAdmin(request):
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    userIsAdmin = False
    if userInfo.admin == True:
        userIsAdmin = True
        
    #Gets active polls
    polls = Poll.objects.filter(active=True)
        
    args = {'userIsAdmin':userIsAdmin, 'polls':polls}
    
    return render(request, 'voting/admin.html', args)

def electionAdminResults(request, poll_id):
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    #Does not work if not admin
    if userInfo.admin != True:
        return HttpResponseRedirect('/profile')
    
    userIsAdmin = True
    
    poll = Poll.objects.get(id=poll_id)
    
    #Creates array with question IDs in poll
    questionIDs = []
    questions = Question.objects.filter(poll=poll).order_by('questionOrder')
    for q in questions:
        questionIDs.append(q.id)
    
    #Generates responses for the poll
    responses = Response.objects.filter(poll=poll)
    
    #Generates multi-demential array with all responses for a question in each array
    allPollResponses = []
    for qInArray in range(len(questionIDs)):
        thisQuestionResponses = []
        qID = str(questionIDs[qInArray])
        for R in responses:
            tempResponse = R.response
            for r in tempResponse:
                if r[0] == qID:
                    for i in r[1:]:
                        if i != 'null':
                            thisQuestionResponses.append(i)
        allPollResponses.append(thisQuestionResponses)
    
    #Generates [][] with questions and response counts
    #Uses questionIDs array to find question, paired with allPollResponses 2D array to generate 2D array
    responsesToPrint = []
    for questionX in range(len(allPollResponses)):
        questionID = questionIDs[questionX]
        thisQuestion = Question.objects.get(id=questionID)
        thisQuestionResponses = allPollResponses[questionX]
        thisQuestionCounter = collections.Counter(thisQuestionResponses)
        thisQuestionTop = thisQuestionCounter.most_common(thisQuestion.choicesAccepted + 5)
        
        thisQuestionToPrint = [thisQuestion.name, thisQuestionTop]
        responsesToPrint.append(thisQuestionToPrint)
        
    
    args = {'poll':poll, 'userIsAdmin':userIsAdmin, 'responsesToPrint':responsesToPrint}
    return render(request, 'voting/results.html', args)
    

def profile(request):
    user = request.user
    
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    userIsAdmin = False
    if userInfo.admin == True:
        userIsAdmin = True
        
    
    #Determines user grade/group
    grade = userInfo.gradeLevel
    gradeString = str(grade)
    group = Group.objects.get(name=gradeString)
    
    #Gets current time to see if poll is active
    currentTime = timezone.now()
    
    #polls = Poll.objects.filter(groupsAllowed=group[0], active=True)
    polls = Poll.objects.filter(groupsAllowed=group, active=True, startTime__lte=currentTime, endTime__gte=currentTime)
    
    for x in polls:
        print(str(x.id))
        print(userInfo.votedIN)
        if x.id in userInfo.votedIN:
            print 
            polls = polls.exclude(id=x.id)
            print("Got One!")
    
    args = {'user':user, 'grade':grade, 'polls':polls, 'userIsAdmin':userIsAdmin}

    return render(request, 'voting/profile.html', args)

def error(request):
    return render(request, 'voting/failed.html')

def submit(request, poll_id, maxChoicesAccepted):
    user = request.user
    poll = Poll.objects.get(id=poll_id)
    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    
    '''
    currentTime = timezone.now()
    
    if poll.endTime < currentTime or poll.startTime > currentTime:
        return HttpResponseRedirect('/responseError')
    '''
    
    #Determines user grade/group
    grade = userInfo.gradeLevel
    gradeString = str(grade)
    group = Group.objects.get(name=gradeString)
    
    currentTime = timezone.now()
    allowedPolls = Poll.objects.filter(groupsAllowed=group, active=True, startTime__lte=currentTime, endTime__gte=currentTime)
    
    if poll not in allowedPolls:
        return HttpResponseRedirect('/responseError')
    
    '''
    
    allowed = False
    for x in allowedPolls:
        if x.id == poll_id:
            allowed = True
            
    if not allowed:
            return HttpResponseRedirect('/responseError')
            
    '''

    
    if poll_id in userInfo.votedIN:
        return HttpResponseRedirect('/responseError')
    
    if request.method == 'POST':
        submission = request.POST
    else:
        return HttpResponseRedirect('/responseError')
    
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
            
            #Makes multidementional array not crap itself
            while currentResponse.__len__() < maxChoicesAccepted:
                currentResponse.append('null')
                
            responses.append(currentResponse)
            
    print(responses)
            #print(x)
            #print(submission.get(x))
            
    #Create instance in Response model
    Response.objects.create(user=user, poll=poll, response=responses)
    
    #Adds poll to user's votedIN
    userInfo.votedIN.append(poll_id)
#FIXME uncomment
    userInfo.save()
    
#FIXME remove comment
    logout(request)
    return HttpResponseRedirect('/success')

def poll(request, poll_id):
    user = request.user

    #Gets extra info on user
    userInfo = UserInfo.objects.get(user=user)
    
    if poll_id in userInfo.votedIN:
        return HttpResponseRedirect('/responseError')

    try:
        thisPoll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Ballot does not exist")
        
    pollName = thisPoll.name
        
    questions = Question.objects.filter(poll=thisPoll).order_by('questionOrder')
    
    #Finds the most number of responses accepted in any question
    maxLengthFinder = questions.order_by('-choicesAccepted')
    print(maxLengthFinder)
    maxLength = maxLengthFinder[0].choicesAccepted + 1
    
        
    args = {'pollName':pollName, 'user':user, 'questions': questions, 'maxLength':maxLength}
    return render(request, 'voting/poll.html', args)

