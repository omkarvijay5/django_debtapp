from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from users import forms
from django.http import HttpResponseRedirect, HttpResponse
# Create your views here.

class UserRegistrationView(generic.edit.FormView):
	form_class = forms.UserRegistrationForm
	template_name = 'users/registration_form.html'


	def form_valid(self, form):
		new_user = form.save(commit= False)
		new_user.set_password(new_user.password)
		new_user.save()
		self.kwargs['username'] = new_user.username 
		return super(UserRegistrationView, self).form_valid(form)

	def get_success_url(self):
		username = self.kwargs['username']
		return reverse('user_details', kwargs={'username': username})

register = UserRegistrationView.as_view()


class DetailsView(generic.DetailView):
	template_name = 'users/details.html'
	context_object_name = 'new_user'

	def get_object(self, queryset=None):
		username = self.kwargs['username']
		new_user = User.objects.get(username__exact=username)
		return new_user

details = DetailsView.as_view()

class LoginView(generic.FormView):
	template_name = 'users/login.html'
	form_class = forms.UserLoginForm 

	def form_valid(self, form):
		username = form.cleaned_data['name']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(self.request, user)
				return HttpResponseRedirect(reverse('user_details', kwargs={'username': user.username}))
			else:
				#"disabled account error message"
		else:
			return HttpResponseRedirect(reverse('user_signin'))


user_login = LoginView.as_view()


