from django.urls import path
from . import views

urlpatterns = [
    # List of routes (authentication not included)
    path('', views.get_routes),

    # Authentication
    path('auth/signup/', views.UserCreate.as_view(), name="signup"),
    path('auth/login/', views.UserLogin.as_view(), name="login"),


    path('<int:user_id>/bookmarks/',
         views.user_bookmark_view, name='user_bookmark_view'),
    path('users/<int:user_id>/bookmarks/<int:bookmark_id>',
         views.patch_bookmark_view, name='user_bookmark_view'),
    
]
