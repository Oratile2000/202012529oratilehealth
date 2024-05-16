from rest_framework import serializers
from .models import User
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

# form for registering users or receiving user input data
class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ['id', 'username', 'email', 'password1', 'password2', 'first_name', 'last_name']


# form for receiving user input data to update user details
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]
        extra_kwargs = {'username': {'required': False},
                        'password': {'required': False}}


# form for logging in users
class LoginSerializer(LoginSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']