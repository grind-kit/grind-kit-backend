from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import InstanceContent, Job, Account

admin.site.register(InstanceContent)
admin.site.register(Job)

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'UserProfiles'

class CustomizedUserAdmin (UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
admin.site.register(Account)