from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('users', views.create_user, name='create_user'),
    path('users/<str:username>', views.user_info_view, name='user_info_view'),
]
