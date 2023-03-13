from rest_framework import serializers

from accounts.models import MovieList, MoviesToRecommend, User,RatedMovies



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
      model = User
      fields=['email', 'name','password', 'password2']
      extra_kwargs={
        'password':{'write_only':True}
      }
      
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']


class RatedMoviesSerializer(serializers.ModelSerializer):
   class Meta:
      model = RatedMovies
      fields = ['movie','user','rating']

class MovieToRecommendSerializer(serializers.ModelSerializer):
   class Meta:
      model = MovieList
      fields = ['id','Title','Year','Genre1','Genre2','Genre3','Director','Cast1','Cast2','Cast3','Cast4']
