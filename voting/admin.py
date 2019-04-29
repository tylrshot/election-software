from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

from voting.models import Poll, Question, Group, Student, UserInfo, Choice, Response

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class UserInfoResource(resources.ModelResource):
    class Meta:
        model = UserInfo
        fields = ('user', 'gradeLevel',)

class UserInfoAdmin(ImportExportModelAdmin):
    resource_class = UserInfoResource

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Choice)
admin.site.register(Response)

admin.site.unregister(User)

class UserResource(resources.ModelResource):
    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'password',)

class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')


admin.site.register(User, UserAdmin)
