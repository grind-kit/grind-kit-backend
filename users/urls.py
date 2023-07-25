from django.urls import path
from . import views

urlpatterns = [
    # List of routes (authentication not included)
    path('', views.get_routes),

    # Authentication
    path('auth/signup/', views.UserCreate.as_view(), name="signup"),
    path('auth/login/', views.UserLogin.as_view(), name="login"),

    # User object
#     path('me/', views.UserGet.as_view(), name='get-user'),
    path('me/', views.UserUpdate.as_view(), name='update-user'),

    # Bookmarks
    path('<int:user_id>/bookmarks/',
         views.UserBookmarkListCreate.as_view(), name='list-create-bookmark'),
    path('<int:user_id>/bookmarks/<int:bookmark_id>',
         views.UserBookmarkRetrieveUpdate.as_view(), name='retrieve-update-bookmark'),
    
]
