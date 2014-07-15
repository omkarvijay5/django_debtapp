from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.contrib.auth.models import User
from registration.signals import user_registered
# Create your models here.

class Friendship(models.Model):
    user = models.ForeignKey(User, related_name="me")
    friend = models.ForeignKey(User)
    net_amount = models.IntegerField(null=True, blank=True)
    owe = models.IntegerField(null=True, blank=True)


class Transaction(models.Model):
    history = models.ForeignKey(User, related_name="transactions")
    owe_id = models.IntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)

class UserProfile(models.Model):
    profile = models.OneToOneField(User, primary_key=True)
    image = models.ImageField(upload_to='/static/users/images/', default='static/users/images/gravatar.jpg')

def add_login_message(sender, user, request, **kwargs):
    messages.success(request, "You have successfully logged in!")
    return messages

user_logged_in.connect(add_login_message)


def add_image_to_user(sender, user, request, **kwargs):
    user_profile = UserProfile.objects.create(profile=user)
    user_profile.save()
    return user_profile

user_registered.connect(add_image_to_user)
