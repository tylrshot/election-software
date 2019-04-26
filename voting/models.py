from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gradeLevel = models.IntegerField(blank=True, null=True)
    votedIN = ArrayField(models.IntegerField(default=0, blank=True), blank=True, null=True)
    
@receiver(post_save, sender=User)
def create_user_userinfo(sender, instance, created, **kwargs):
    if created:
        UserInfo.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_userinfo(sender, instance, **kwargs):
    instance.userinfo.save()
    
    
class Poll(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True, null=True)
    
    active = models.BooleanField(default=False)
    startTime = models.DateTimeField(blank=True, null=True)
    endTime = models.DateTimeField(blank=True, null=True)
    
    groupsAllowed = models.ManyToManyField('Group', blank=True, default='None')
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    
    def __str__(self):
        return '{0}'.format(self.name)
    
class Question(models.Model):
    poll = models.ForeignKey('Poll', models.CASCADE)
    name = models.CharField(max_length=100)
    questionOrder = models.IntegerField(default=0)
    
    choices = ArrayField(models.CharField(max_length=100), null=True)
    choicesAccepted = models.IntegerField(default=1)
    
    #Question Types
    MULTI_CHOICE = 'MC'
    RANKED = 'RA'
    TOPX = 'TX'
    QUESTION_TYPES = (
        (MULTI_CHOICE, 'Multiple Choice'),
        (RANKED, 'Ranked'),
        (TOPX, 'Top X'),
    )
    questionType = models.CharField(
        max_length=2,
        choices=QUESTION_TYPES,
        default=MULTI_CHOICE,
    )
    #result =
    
    def __str__(self):
        return '{0}'.format(self.name)
    
class Choice(models.Model):
    question = models.ForeignKey('Question', models.CASCADE)
    name = models.CharField(max_length=100)
    choiceOrder = models.IntegerField(default=0)
    
    votes = models.IntegerField(default=0, blank=True)
    
    def __str__(self):
        return '{0}'.format(self.name)
    
    
class Response(models.Model):
    dateTime = models.DateTimeField(auto_now_add=True, null=True)
    
    user = models.ForeignKey(User, models.CASCADE)
    poll = models.ForeignKey('Poll', models.CASCADE)
    #[Question order, Choice order, Question order, Choice order]
    response = ArrayField(models.IntegerField(default=0, blank=True), blank=True, null=True)
    
    
class Group(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField('Student', blank=True, default='None')
    
class Student(models.Model):
    firstName = models.CharField(max_length=35)
    lastName = models.CharField(max_length=35)
    gradeLevel = models.IntegerField()
    
    #Genders
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.CharField(
        max_length=1,  
        choices=GENDERS,
        null=True,
        blank=True,
    )
    

    
    
