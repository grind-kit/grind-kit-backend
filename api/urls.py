from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('conditions', views.get_content_finder_conditions, name='get_content_finder_conditions'),
]
