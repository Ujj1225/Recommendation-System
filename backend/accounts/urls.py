from django.urls import path
from accounts.views import MovieToRecomendView, UserLoginView, UserProfileView, UserRegistrationView, RatedMovieView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('ratemovie/',RatedMovieView.as_view(),name='ratemovie'),
    path('movietorecommend/',MovieToRecomendView.as_view(),name='movietorecommend'),
]