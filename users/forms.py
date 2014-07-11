from django.contrib.auth.models import User
from django import forms

class FriendEmailForm(forms.Form):
	friend_email = forms.EmailField(required=True)