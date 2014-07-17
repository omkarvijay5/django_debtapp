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
        owe_user = User.objects.get(pk=transaction.owe_id)
        return "I owe %s"% owe_user.username
    else:
        owe_user = User.objects.get(pk=transaction.owe_id)
        return "%s Owes me"% owe_user.username