from django.contrib import admin

from .models import FirebaseUser, Bookmark

admin.site.register(FirebaseUser)
admin.site.register(Bookmark)