from django.views import generic
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from users.models import Friendship, UserProfile
from users import forms
# from django.dispatch import receiver

# Create your views here.


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AjaxTemplateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'upload_image.html'):
            split = self.template_name.split('.html')
            split[-1] = '_ajax'
            split.append('.html')
            self.ajax_template_name = ''.join(split)
        if request.is_ajax():
            self.template_name = self.ajax_template_name
        return super(AjaxTemplateMixin, self).dispatch(
            request, *args, **kwargs)


class AddFriendView(LoginRequiredMixin, generic.edit.FormView):
    form_class = forms.FriendEmailForm
    template_name = 'users/email_form.html'

    def form_valid(self, form):
        friend_email = form.cleaned_data['friend_email']
        friend = User.objects.get(email__exact=friend_email)
        user = self.request.user
        friendship = Friendship.objects.create(user=user, friend=friend)
        reverse_friendship = Friendship.objects.create(
            user=friend,
            friend=user)
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
            user = get_object_or_404(User, username__exact=username)
        else:
            user = self.request.user
        return user

user_details = UserDetails.as_view()


class UserFriendsView(LoginRequiredMixin, generic.ListView):
    template_name = "users/user_friends.html"
    context_object_name = 'friends'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        self.user = user
        friendships = Friendship.objects.filter(user__exact=user)
        if friendships:
            friends = [friendship.friend for friendship in friendships]
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
        split_amount = amount / len(friends)
        friends = [User.objects.get(username=friend) for friend in friends]
        friendships = Friendship.objects.filter(
            user__exact=paid_user).filter(
            friend__in=friends)
        for friendship in friendships:
            reverse_friendship = Friendship.objects.get(user=friendship.friend,
                                                        friend=paid_user)
            if not friendship.owe:
                friendship.owe = friendship.friend.id
                friendship.net_amount = split_amount
                reverse_friendship.owe = friendship.friend.id
                reverse_friendship.net_amount = split_amount
            elif friendship.owe == paid_user.id:
                settled_amount = friendship.net_amount - split_amount
                friendship.split_bill(settled_amount, friendship,
                                      reverse_friendship, split_amount)
            elif friendship.user.id == paid_user.id:
                settled_amount = friendship.net_amount + split_amount
                friendship.split_bill(settled_amount, friendship,
                                      reverse_friendship, split_amount)
            reverse_friendship.transactions.create(
                amount=split_amount,
                owe_id=reverse_friendship.user.id,
                item=item)
            friendship.transactions.create(amount=split_amount,
                                           owe_id=friendship.friend.id,
                                           item=item)
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
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        transactions = []
        friendships = Friendship.objects.filter(user__exact=user)
        for friendship in friendships:
            for transaction in friendship.transactions.all():
                transactions.append(transaction)
        return transactions

user_history = UserHistoryView.as_view()


class DebtDetails(LoginRequiredMixin, generic.ListView):
    template_name = 'users/user_debt.html'

    def get_queryset(self):
        user = self.request.user
        friendships = Friendship.objects.filter(user__exact=user)
        return friendships

    def get_context_data(self, *args, **kwargs):
        context = super(DebtDetails, self).get_context_data(**kwargs)
        friendships = self.get_queryset()
        user = self.request.user
        i_owe_friends = friendships.filter(owe=user.id)
        iowe_net_sum = i_owe_friends.aggregate(Sum('net_amount'))
        friends_owe_me = friendships.exclude(owe=user.id)
        friends_owe_sum = friends_owe_me.aggregate(Sum('net_amount'))
        histories = []
        for friendship in friendships:
            for transaction in friendship.transactions.all():
                histories.append(transaction)
        payload = {'i_owe_friendships': i_owe_friends,
                   'friend_owe_friendships': friends_owe_me,
                   'histories': histories}
        context.update(payload)
        context['i_owe_amount'] = iowe_net_sum['net_amount__sum']
        context['friends_owe_amount'] = friends_owe_sum['net_amount__sum']
        return context

net_amount_details = DebtDetails.as_view()


class UserImageView(LoginRequiredMixin, AjaxTemplateMixin,
                    generic.edit.UpdateView):
    model = User
    template_name = 'users/upload_image.html'
    form_class = forms.UserImageForm
    success_url = '/'

    def get_object(self):
        username = self.kwargs['username']
        user = User.objects.get(username=username)
        try:
            userprofile = user.userprofile
        except:
            userprofile = UserProfile.objects.create(profile=user)

        return userprofile


user_image = UserImageView.as_view()
