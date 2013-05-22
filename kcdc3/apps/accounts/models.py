from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile

class ExtendedProfile(UserenaBaseProfile):
	user = models.OneToOneField(User, unique=True)
	phone_number = models.CharField(max_length=32, blank=True, null=True)
	zipcode = models.CharField(max_length=5, blank=True, null=True)

