from django.urls import path
from accounts.views import UserLoginView, UserProfileView, UserRegistrationView, RatedMovieView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('ratemovie/',RatedMovieView.as_view(),name='ratemovie'),
]