from django_debtapp import UserProfile
from dhango.contrib.auth.models import UserProfile
from django import forms


class UserRegistrationForm(forms.ModelForm):
	password_confirmation = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = UserProfile
		fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation',)