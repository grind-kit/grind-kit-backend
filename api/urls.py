from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('users', views.create_user, name='create_user'),
    path('users/<str:username>', views.user_info_view, name='user_info_view'),
    path('users/<int:user_id>/bookmarks', views.user_bookmark_view, name='user_bookmark_view'),
    path('conditions', views.get_content_finder_conditions, name='get_content_finder_conditions'),
]
