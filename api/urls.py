from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('users', views.create_user),
]
