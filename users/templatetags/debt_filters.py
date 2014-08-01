from django import template
from django.contrib.auth.models import User
register = template.Library()


@register.assignment_tag
def show_users():
    users = User.objects.all()
    return set(users)


@register.simple_tag
def i_owe_friend(transaction, user):
    if transaction.owe_id == user.id:
        owe_user = transaction.history.friend
        owe_user = User.objects.get(username=owe_user.username)
        return "I owe %s" % owe_user.username
    else:
        owe_user = transaction.history.friend
        owe_user = User.objects.get(username=owe_user.username)
        return "%s Owes me" % owe_user.username
