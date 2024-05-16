from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid

# Create your models here.
class User(AbstractUser):
	# using uuids as the primary key or ID
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)