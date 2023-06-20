from django.contrib import admin
from .models import FirebaseUser, FirebaseUserToken

admin.site.register(FirebaseUser)
admin.site.register(FirebaseUserToken)