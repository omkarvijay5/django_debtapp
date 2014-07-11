from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
# Create your models here.

class Friendship(models.Model):
	user = models.ForeignKey(User, related_name="me")
	friend = models.ForeignKey(User, related_name="friends")
	net_amount = models.IntegerField(null=True, blank=True)
	owe = models.IntegerField(null=True, blank=True)

def add_login_message(sender, user, request, **kwargs):
	messages.success(request, "You have successfully logged in!")
	return messages

user_logged_in.connect(add_login_message)