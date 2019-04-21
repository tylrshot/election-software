from django.contrib import admin

# Register your models here.

from voting.models import Poll, Question, Group, Student, UserVotes

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(UserVotes)