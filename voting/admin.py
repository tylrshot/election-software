from django.contrib import admin

# Register your models here.

from voting.models import Poll, Question, Group, Student, UserInfo, Choice, Response

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(UserInfo)
admin.site.register(Choice)
admin.site.register(Response)