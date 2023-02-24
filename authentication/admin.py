from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

# admin.site.register(CustomUserModel) #CustomerUser Model
admin.site.register(InstanceContent) #Instance contents Model
admin.site.register(Job) #Jobs Model