from django.test  import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from users.models import Friendship
from users.views import AddFriendView, UserDetails

# Create your tests here.

class FriendshipTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.factory = RequestFactory()
        self.friend = User.objects.create_user(username='userfriend', email='user_friend@gmail.com',password='temporary')
        self.friend.is_active=True
    
    def test_add_friend_redirect(self):
        "check if user logged in if not redirects to the login page"
        "user does not logged in, redirects to login page"
        response = self.c.get(reverse('friend_email_form'))
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse('friend_email_form'),{'friend_email': 'user_friend@gmail.com'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse('friend_email_form'),{'friend_email':'invalidemail@gmail.com'})
        self.assertEqual(response.status_code, 302)

        "testing for user logged in"
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('friend_email_form'))
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse('friend_email_form'),{'friend_email': 'user_friend@gmail.com'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse('friend_email_form'), {'friend_email': 'invalidemail@gmail.com'})
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse('friend_email_form'), {'friend_email': 'xyyz'})
        self.assertEqual(response.status_code, 200)

    def test_user_details_view(self):
        "check for login"
        response = self.c.get(reverse('debt_user_details', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('debt_user_details', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('debt_user_details', kwargs={'username': self.friend.username}))
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('debt_user_details', kwargs={'username': 'invalidusername'}))
        self.assertEqual(response.status_code, 404)

    def test_user_friends_view(self):
        "checks for valid url or else returns 404"
        "testing for current user url"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        "testing for friend url"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.friend.username}))
        self.assertEqual(response.status_code, 200)
        "testing for invalid url"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': 'invaliduser'}))
        self.assertEqual(response.status_code, 404)

    def test_pagination_user_friends_view(self):
        "checks for pagination functionality"
        num_friends = 10
        "creating users and friends"
        for num in range(num_friends):
            new_user = User.objects.create(username="temporary"+str(num), password='testpassword')
            Friendship.objects.create(user=self.user, friend=new_user)
            Friendship.objects.create(user=new_user, friend=self.user)
        self.assertEqual(User.objects.count(),12)
        self.assertEqual(Friendship.objects.count(), 20)
        "testing for pagination"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username})+'?page=1')
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username})+'?page=1')
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username})+'?page=2')
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username})+'?page=3')
        self.assertEqual(response.status_code, 404)

    def test_split_amount_view(self):
        "testing valid form"
        response = self.c.get(reverse('debt_split_amount'))
        self.assertEqual(response.status_code, 302)
        "user login"
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('debt_split_amount'))
        self.assertEqual(response.status_code, 200)

