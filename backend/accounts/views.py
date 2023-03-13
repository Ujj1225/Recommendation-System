from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import  RatedMoviesSerializer, UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer
from django.contrib.auth import authenticate
from accounts.renderers import UserRenderer
from accounts.models import MovieList, MoviesToRecommend,RatedMovies
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .tree_filter import recommended_movies, priority



# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        email=serializer.data.get('email')
        name=serializer.data.get('name')
        return Response({'token':token,'email':email,'name':name,'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  

class RatedMovieView(APIView):
  renderer_classes=[UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self,request,format=None):
    serializer = RatedMoviesSerializer(request.data)
    serializer.is_valid(raise_exception=True)
    movie = serializer.data.get('movie')
    rating = serializer.data.get('rating')
    query1 = MoviesToRecommend.objects.all().filter(user=request.user,priority='3s')
    lst1=[]
    for query in query1:
      lst1.append(query.movie)
    query2 = MoviesToRecommend.objects.all().filter(user=request.user,priority='4s')
    lst2=[]
    for query in query2:
      lst2.append(query.movie)
    query3 = MoviesToRecommend.objects.all().filter(user=request.user,priority='5s')
    lst3=[]
    for query in query3:
      lst3.append(query.movie)
    final_list=[lst1,lst2,lst3]
    
    # calling fuction to generate recommendations and update database MoviesToRecommend
    new_priority_list = priority(final_list, movie, rating)
      #update list

    mov_lst=[1,2,3]
    movies_query = MovieList.objects.all().filter(pk__in=mov_lst)
    serializer = MoviesToRecommend(movies_query)
    return Response(serializer.data,status=status.HTTP_200_OK)