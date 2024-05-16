from rest_framework import permissions, status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from .models import User
from .serializers import UserSerializer, LoginSerializer, UserUpdateSerializer
from rest_framework.authtoken.models import Token

# user register view
class UserRegistrationView(RegisterView): # overriding the register view to facilitate the creation of tokens on user registration

	permission_classes = [permissions.AllowAny] # allow anyone to access the register view

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		
		user = self.perform_create(serializer) # get the user making the request

		try:
			token, created = Token.objects.get_or_create(user=user) # create a token for the user
		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

		return Response({'token': token.key}, status=status.HTTP_201_CREATED)

	def perform_create(self, serializer):
		return serializer.save(self.request) # assign user to the incoming request


# user login view
class UserLoginView(LoginView):

	serializer_class = LoginSerializer
	permission_classes = [permissions.AllowAny] # allow anyone to access the login view

	def get_response(self):

		response = super().get_response()

		if response.status_code == status.HTTP_200_OK:
			user = self.user # get the user making the request

			Token.objects.filter(user=user).delete() # delete the existing token to avoid one user having many tokens

			token, created = Token.objects.get_or_create(user=user) # create a token for the user
			
		return Response({'token': token.key}, status=status.HTTP_200_OK)


# update user details view
class UserUpdateView(generics.RetrieveUpdateAPIView):

	serializer_class = UserUpdateSerializer
	permission_classes = [permissions.IsAuthenticated] # allow only authenticated users to access this view

	def get_object(self):
		return self.request.user # return the user details after updating


# current user view
class CurrentUserRetrievalView(APIView):

	permission_classes = [permissions.IsAuthenticated] # allow only authenticated users to access this view

	def get(self, request):

		user = request.user # get the user making the request

		try:
			user_object = User.objects.get(id=user.id)
		except User.DoesNotExist:
			return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

		user_data = {
			'id': user.id,
			'username': user.username,
			'email': user.email,
			'first_name': user.first_name,
			'last_name': user.last_name,
		}

		return Response({'user': user_data,}, status=status.HTTP_200_OK)