from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('login', views.login_view, name='login_view'),
    path('users', views.create_user, name='create_user'),
    path('users/<int:user_id>/bookmarks', views.user_bookmark_view, name='user_bookmark_view'),
    path('users/<int:user_id>/bookmarks/<int:bookmark_id>', views.patch_bookmark_view, name='user_bookmark_view'),
    path('tokens', views.create_user_token, name='create_user_token'),
    path('conditions', views.get_content_finder_conditions, name='get_content_finder_conditions'),
]
