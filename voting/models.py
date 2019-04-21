from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)
    
    
class UserVotes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    votedIN = ArrayField(models.IntegerField(default=0, blank=True), blank=True, null=True)
    
@receiver(post_save, sender=User)
def create_user_uservotes(sender, instance, created, **kwargs):
    if created:
        UserVotes.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_uservotes(sender, instance, **kwargs):
    instance.uservotes.save()
    
    
class Poll(models.Model):
    active = models.BooleanField(default=False)
    groupsAllowed = models.ManyToManyField('Group', blank=True, default='None')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    
class Question(models.Model):
    poll = models.ForeignKey('Poll', models.CASCADE)
    name = models.CharField(max_length=100)
    
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
    

    
    
