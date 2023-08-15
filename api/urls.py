from django.urls import path
from . import views

urlpatterns = [
    # List of routes
    path('', views.get_routes),

    # Content Finder Conditions
    path('conditions', views.ContentFinderConditionList.as_view(), name='list-conditions'),
    path('conditions/<int:pk>/bookmarks/', views.ContentFinderConditionBookmarkList.as_view(), name='list-bookmarks'),
]
