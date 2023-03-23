from django.urls import path
from . import views
from .views import my_view


urlpatterns = [
    path('', views.getRoutes),
    path('user/', my_view)
    ,
]
