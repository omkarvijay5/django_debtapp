from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from users.models import Friendship
from users import forms
# from django.dispatch import receiver

# Create your views here.


class EmailFormView(generic.edit.FormView):
    form_class = forms.FriendEmailForm
    template_name = 'users/email_form.html'

    def form_valid(self, form):
        friend_email = form.cleaned_data['friend_email']
        friend = User.objects.get(email__exact=friend_email)
        user = self.request.user
        friendship = Friendship.objects.create(user=user, friend=friend)
        reverse_friendship = Friendship.objects.create(user=friend, friend=user)
        friendship.save()
        reverse_friendship.save()
        return super(EmailFormView, self).form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('debt_user_friends', kwargs={'username': username})

email_form = EmailFormView.as_view()


class UserDetails(generic.DetailView):
    template_name = 'users/details.html'
    context_object_name = 'new_user'

    def get_object(self):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = User.objects.get(username__exact=username)
        else:
            user = self.request.user
        return user

user_details = UserDetails.as_view()

class UserFriendsView(generic.ListView):
    template_name = "users/user_friends.html"
    context_object_name = 'friends'

    def get_queryset(self):
        username = self.kwargs['username']
        user = User.objects.get(username__exact=username)
        friendships = Friendship.objects.filter(user__exact=user)
        friends = [user.friend for user in friendships]
        return friends

user_friends = UserFriendsView.as_view()


