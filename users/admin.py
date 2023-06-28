from django.contrib import admin
from .models import *

admin.site.register(FirebaseUser)
admin.site.register(FirebaseUserToken)
admin.site.register(UserBookmark)