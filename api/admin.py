from django.contrib import admin

from .models import FirebaseUser, Bookmarks

admin.site.register(FirebaseUser)
admin.site.register(Bookmarks)