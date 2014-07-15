from django.contrib.auth.models import User
from django import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from users.models import Friendship, Transaction

class FriendEmailForm(forms.Form):
    friend_email = forms.EmailField(required=True)

    def clean_friend_email(self):
        email = self.cleaned_data['friend_email']
        try:
            user = get_object_or_404(User,email=email)
        except:
            raise forms.ValidationError("Enter a registered email")
        return email

class SplitBillForm(forms.Form):
    def __init__(self,*args, **kwargs):
        current_user = kwargs.pop('current_user')
        super(SplitBillForm, self).__init__(*args, **kwargs)
        self.fields['paid_user'] = forms.ChoiceField(choices=get_users(current_user), required=False)
        self.fields['users'] = forms.MultipleChoiceField(choices=get_users(current_user), required=False)
    item = forms.IntegerField(required=True)

    class Meta:
        model = Transaction



def get_users(current_user):
    friendships = Friendship.objects.filter(user=current_user)
    if friendships:
        users = [friendship.friend.username for friendship in friendships]
        users.add(current_user)
    else:
        users = []
    return users
