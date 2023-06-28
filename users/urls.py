from django.urls import path
from . import views

urlpatterns = [
    # List of routes (authentication not included)
    path('', views.get_routes),

    # Authentication
    path('auth/signup/', views.UserCreate.as_view(), name="signup"),
    path('auth/login/', views.UserLogin.as_view(), name="login"),

    # Bookmarks
    path('<int:user_id>/bookmarks/',
         views.UserBookmarkListCreate.as_view(), name='listcreate-bookmark'),
    path('<int:user_id>/bookmarks/<int:bookmark_id>',
         views.UserBookmarkUpdate.as_view(), name='update-bookmark'),
    
]
