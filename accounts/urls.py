from .views import UserRegistrationView, UserLoginView,UserUpdateView, CurrentUserRetrievalView
from django.urls import path

urlpatterns = [
	path('register/', UserRegistrationView.as_view()),
	path('update/', UserUpdateView.as_view()),
	path('login/', UserLoginView.as_view()),
	path('user/', CurrentUserRetrievalView.as_view())
]