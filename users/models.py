from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.contrib.auth.models import User

# Create your models here.

class Friendship(models.Model):
	user = models.ForeignKey(User, related_name="me")
	friend = models.ForeignKey(User)
	net_amount = models.IntegerField(null=True, blank=True)
	owe = models.IntegerField(null=True, blank=True)


class Transactions(models.Model):
	history = models.ForeignKey(Friendship, related_name="transactions")
	owe_id = models.IntegerField(null=True, blank=True)
	amount = models.FloatField(null=True, blank=True)

def add_login_message(sender, user, request, **kwargs):
	messages.success(request, "You have successfully logged in!")
	return messages



user_logged_in.connect(add_login_message)
