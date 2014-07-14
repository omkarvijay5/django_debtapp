from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404

class FriendEmailForm(forms.Form):
	friend_email = forms.EmailField(required=True)

	def clean_friend_email(self):
		email = self.cleaned_data['friend_email']
		try:
			user = get_object_or_404(User,email=email)
		except:
			raise forms.ValidationError("Enter a registered email")