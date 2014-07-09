from django.contrib.auth.models import User
from django import forms


class UserRegistrationForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		
	password_confirmation = forms.CharField(widget=forms.PasswordInput())
	password = forms.CharField(widget=forms.PasswordInput())

	def clean_password_confirmation(self):
		password = self.cleaned_data.get('password')
		password_confirmation = self.cleaned_data.get('password_confirmation')
		if password != password_confirmation:
			raise forms.ValidationError("Passwords do not match")
		return password_confirmation

	def clean_email(self):
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Email has already been taken")
		return email

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_confirmation',)

class UserLoginForm(forms.ModelForm):
	name = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	password_confirmation = forms.CharField(widget=forms.PasswordInput())
	
	class Meta:
		model = User
		fields = ('name', 'password', 'password_confirmation',)
