from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		
	password_confirmation = forms.CharField(widget=forms.PasswordInput())
	password = forms.CharField(widget=forms.PasswordInput())


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation',)