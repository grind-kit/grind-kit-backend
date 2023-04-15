from django.contrib import admin

from .models import FirebaseUser, Bookmark, ContentFinderCondition

admin.site.register(FirebaseUser)
admin.site.register(Bookmark)
admin.site.register(ContentFinderCondition)