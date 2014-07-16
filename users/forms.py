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

def get_users(current_user):
    current_user = User.objects.get(username__exact=current_user.username)
    friendships = Friendship.objects.filter(user__exact=current_user)
    if friendships:
        users = [(friendship.friend, friendship.friend) for friendship in friendships]
        users.append(tuple([current_user, current_user]))
    else:
        users = tuple([current_user,current_user])
    return users

class SplitBillForm(forms.Form):
    def __init__(self,*args, **kwargs):
        current_user = kwargs.pop('current_user')
        super(SplitBillForm, self).__init__(*args, **kwargs)
        self.fields['paid_user'] = forms.ChoiceField(choices=get_users(current_user))
        self.fields['paid_user'].label = "Who paid?"
        self.fields['friends'] = forms.MultipleChoiceField( choices=get_users(current_user), 
                                                            widget=forms.CheckboxSelectMultiple()
                                                        )
        self.fields['friends'].label = "Friends whom you want to share"
    item = forms.CharField(label="For What?", 
                              widget=forms.TextInput(attrs={'placeholder': "ex: burger and petrol"})
                            )
    amount = forms.IntegerField(label="How much?",
                              widget=forms.TextInput(attrs={'placeholder': "ex: 100 and 500"}) 
                              )

    class Meta:
        model = Transaction
