from django.contrib.auth import get_user_model
from django import forms
User = get_user_model()

class FriendEmailForm(forms.Form):
	friend_email = forms.EmailField(required=True)