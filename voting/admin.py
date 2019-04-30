from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

from voting.models import Poll, Question, Group, UserInfo, Response

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserInfoResource(resources.ModelResource):
    class Meta:
        model = UserInfo
        fields = ('user', 'gradeLevel',)

class UserInfoAdmin(ImportExportModelAdmin):
    list_display = ('user', 'gradeLevel', 'admin', 'id')
    resource_class = UserInfoResource
    
class PollAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'startTime', 'endTime', 'active')
    pass

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'poll', 'id', 'questionType', 'choicesAccepted', 'questionOrder')
    pass

class ResponseAdmin(admin.ModelAdmin):
    list_display = ('poll', 'user', 'id')
    pass

admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Group)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Response, ResponseAdmin)

admin.site.unregister(User)

class UserResource(resources.ModelResource):
    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'password',)

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('username', 'id', 'is_active', 'date_joined', 'is_staff')


admin.site.register(User, UserAdmin)
