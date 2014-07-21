from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from users.models import Friendship, Transaction
from users import forms
# from django.dispatch import receiver

# Create your views here.

class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class AddFriendView(LoginRequiredMixin, generic.edit.FormView):
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
        return super(AddFriendView, self).form_valid(form)

    def get_success_url(self):
        username = self.request.user.username
        return reverse('debt_user_friends', kwargs={'username': username})

add_friend = AddFriendView.as_view()


class UserDetails(LoginRequiredMixin, generic.DetailView):
    template_name = 'users/details.html'
    context_object_name = 'new_user'

    def get_object(self):
        if 'username' in self.kwargs:
            username = self.kwargs['username']
            user = get_object_or_404(User,username__exact=username)
        else:
            user = self.request.user
        self.kwargs['new_user'] = user
        return user

    def get_context_data(self, *args, **kwargs):
        context = super(UserDetails, self).get_context_data(**kwargs)
        user = self.kwargs['new_user']
        friendships = Friendship.objects.filter(user__exact=user)
        context['friendships'] = friendships
        histories = [transaction for friendship in friendships for transaction in friendship.transactions.all()]
        context.update({'histories': histories})
        return context

user_details = UserDetails.as_view()

class UserFriendsView(LoginRequiredMixin,generic.ListView):
    template_name = "users/user_friends.html"
    context_object_name = 'friends'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        self.user = user
        friendships = Friendship.objects.filter(user__exact=user)
        if friendships:
            friends = [user.friend for user in friendships]
        else:
            friends = []
        return friends

user_friends = UserFriendsView.as_view()


class SplitAmountView(LoginRequiredMixin, generic.FormView):
    template_name = "users/amount_form.html"
    form_class = forms.SplitBillForm
    context_object_name = 'friends'

    def get_form_kwargs(self):
        kwargs = super(SplitAmountView, self).get_form_kwargs()
        kwargs.update({'current_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        item = form.cleaned_data['item']
        friends = form.cleaned_data['friends']
        paid_username = form.cleaned_data['paid_user']
        paid_user = get_object_or_404(User, username=paid_username)
        split_amount = amount/len(friends)
        friendships = Friendship.objects.filter(user__exact=paid_user)
        for friendship in friendships:
            reverse_friendship = Friendship.objects.get(user=friendship.friend,friend=paid_user)
            if not friendship.owe:
                friendship.owe = friendship.friend.id
                friendship.net_amount = split_amount
                reverse_friendship.owe = friendship.friend.id
                reverse_friendship.net_amount = split_amount
            elif friendship.owe == paid_user.id:
                settled_amount = friendship.net_amount - split_amount 
                friendship.split_bill(settled_amount, friendship, reverse_friendship, split_amount)
            elif friendship.user.id == paid_user.id:
                settled_amount = friendship.net_amount + split_amount
                friendship.split_bill(settled_amount, friendship, reverse_friendship, split_amount)
            reverse_friendship.transactions.create(amount=split_amount, owe_id=paid_user.id, item=item)
            friendship.transactions.create(amount=split_amount, owe_id=paid_user.id, item=item)
            friendship.save()
            reverse_friendship.save()
        return super(SplitAmountView, self).form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse('debt_user_history', kwargs={'username': user})

    def get_context_data(self, *args, **kwargs):
        context = super(SplitAmountView, self).get_context_data(**kwargs)
        user = self.request.user
        friends = user.friendship_set.all()
        context['friends'] = friends
        return context

split_amount = SplitAmountView.as_view()



class UserHistoryView(generic.ListView):
    template_name = 'users/user_history.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        username=self.kwargs['username']
        user = get_object_or_404(User, username=username)
        transactions = []
        friendships = Friendship.objects.filter(user__exact=user)
        for friendship in friendships:
            for transaction in friendship.transactions.all():
                transactions.append(transaction)
        return transactions

user_history = UserHistoryView.as_view()


class DebtDetails(generic.ListView):
    template_name='users/user_debt.html'
    context_object_name = 'friendships'

    def get_queryset(self):
        user = self.request.user
        friendships = Friendship.objects.filter(user__exact=user)
        return friendships

    def get_context_data(self, *args, **kwargs):
        context = super(DebtDetails, self).get_context_data(**kwargs)
        friendships = self.get_queryset()
        histories = [transaction for friendship in friendships for transaction in friendship.transactions.all()]
        context.update({'histories': histories})
        return context

user_debt_details = DebtDetails.as_view()

