from django.test  import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
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
        response = self.c.get(reverse('friend_email_form'))
        self.assertEqual(response.status_code, 302)
        "checking for user logged in"
        request = self.factory.get('/users/email/')
        request.user = self.user
        response = AddFriendView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        "testing for valid email friend"
        response = self.c.post(reverse('friend_email_form'),{'friend_email': 'user_friend@gmail.com'})
        self.assertEqual(response.status_code, 302)
        "testing for invalid email friend"
        response = self.c.post(reverse('friend_email_form'),{'friend_email': 'invalidemail@gmail.com'})
        self.assertEqual(response.status_code,302)
        "testing with registered user but inactive"
        self.new_friend = User.objects.create(username='newfriend',email='validemail@gmail.com',password='password')
        respone = self.c.post(reverse('friend_email_form'), {'friend_email': 'validemail@gmail.com'})
        self.assertEqual(response.status_code,302)

    def test_user_details_view(self):
        "checks for the valid url or else returns 404"
        "testing for valid users without login"
        response = self.c.get(reverse('debt_user_details', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        "testing for accessing friend url"
        response = self.c.get(reverse('debt_user_details', kwargs={'username': self.friend}))
        self.assertEqual(response.status_code, 200)
        "testing valid user with login"
        request = self.factory.get(reverse('debt_user_details', kwargs={'username': self.user.username}))
        request.user = self.user
        response = UserDetails.as_view()(request)
        self.assertEqual(response.status_code, 200)
        "testing accessing friend url with login"
        response = self.c.get(reverse('debt_user_details', kwargs={'username': self.friend.username}))
        self.assertEqual(response.status_code, 200)
        "Accessing invalid url"
        response = self.c.get(reverse('debt_user_details', kwargs={'username': 'invaliduser'}))
        self.assertEqual(response.status_code, 404)

    def test_user_friends_view(self):
        "checks for valid url or else returns 404"
        "testing for current user url"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        "testing for friend url"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': self.friend.username}))
        self.assertEqual(response.status_code, 200)
        "testing for invalid url"
        response = self.c.get(reverse('debt_user_friends', kwargs={'username': 'invaliduser'}))
        self.assertEqual(response.status_code, 404)






