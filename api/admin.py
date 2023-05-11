from django.contrib import admin

from .models import *

admin.site.register(FirebaseUser)

admin.site.register(ContentFinderCondition)
admin.site.register(InstanceContentBookmark)