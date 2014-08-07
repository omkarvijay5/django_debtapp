from PIL import Image
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from users.models import Friendship, Transaction
# Create your tests here.


class FriendshipTestCase(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(
            'temporary', 'temporary@gmail.com', 'temporary')
        self.factory = RequestFactory()
        self.friend = User.objects.create_user(
            username='userfriend', email='user_friend@gmail.com',
            password='temporary')
        self.friend.is_active = True

    def test_add_friend_redirect(self):
        "check if user logged in if not redirects to the login page"
        "user does not logged in, redirects to login page"
        response = self.c.get(reverse('friend_email_form'))
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse(
            'friend_email_form'), {'friend_email': 'user_friend@gmail.com'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse(
            'friend_email_form'), {'friend_email': 'invalidemail@gmail.com'})
        self.assertEqual(response.status_code, 302)

        "testing for user logged in"
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('friend_email_form'))
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'friend_email_form'), {'friend_email': 'user_friend@gmail.com'})
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse(
            'friend_email_form'), {'friend_email': 'invalidemail@gmail.com'})
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'friend_email_form'), {'friend_email': 'xyyz'})
        self.assertEqual(response.status_code, 200)

    def test_user_details_view(self):
        "check for login"
        response = self.c.get(reverse(
            'debt_user_details', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse(
            'debt_user_details', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse(
            'debt_user_details', kwargs={'username': self.friend.username}))
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse(
            'debt_user_details', kwargs={'username': 'invalidusername'}))
        self.assertEqual(response.status_code, 404)

    def test_user_friends_view(self):
        "checks for valid url or else returns 404"
        "testing for current user url"
        response = self.c.get(reverse(
            'debt_user_friends', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse(
            'debt_user_friends', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        "testing for friend url"
        response = self.c.get(reverse(
            'debt_user_friends', kwargs={'username': self.friend.username}))
        self.assertEqual(response.status_code, 200)
        "testing for invalid url"
        response = self.c.get(reverse(
            'debt_user_friends', kwargs={'username': 'invaliduser'}))
        self.assertEqual(response.status_code, 404)

    def test_pagination_user_friends_view(self):
        "checks for pagination functionality"
        num_friends = 10
        "creating users and friends"
        for num in range(num_friends):
            new_user = User.objects.create(
                username="temporary"+str(num), password='testpassword')
            Friendship.objects.create(user=self.user, friend=new_user)
            Friendship.objects.create(user=new_user, friend=self.user)
        self.assertEqual(User.objects.count(), 12)
        self.assertEqual(Friendship.objects.count(), 20)
        "testing for pagination"
        response = self.c.get(reverse(
            'debt_user_friends',
            kwargs={'username': self.user.username})+'?page=1')
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse(
            'debt_user_friends',
            kwargs={'username': self.user.username})+'?page=1')
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse(
            'debt_user_friends',
            kwargs={'username': self.user.username})+'?page=2')
        self.assertEqual(response.status_code, 200)
        response = self.c.get(reverse(
            'debt_user_friends',
            kwargs={'username': self.user.username})+'?page=3')
        self.assertEqual(response.status_code, 404)

    def test_split_amount_view(self):
        "testing valid form"
        response = self.c.get(reverse('debt_split_amount'))
        self.assertEqual(response.status_code, 302)
        "user login"
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('debt_split_amount'))
        self.assertEqual(response.status_code, 200)
        num_friends = 2
        "creating friends"
        for num in range(num_friends):
            new_user = User.objects.create(
                username='test'+str(num), password='test')
            Friendship.objects.create(user=self.user, friend=new_user)
            Friendship.objects.create(user=new_user, friend=self.user)
        test_user = User.objects.get(username='test0')
        test_user_1 = User.objects.get(username='test1')
        Friendship.objects.create(user=test_user, friend=test_user_1)
        Friendship.objects.create(user=test_user_1, friend=test_user)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': '', 'amount': 10, 'paid_user': self.friend,
             'friends': []})
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': None, 'paid_user': self.friend,
             'friends': []})
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 10, 'paid_user': self.friend,
             'friends': []})
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 10, 'paid_user': '',
             'friends': self.user.username})
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 10, 'paid_user': self.user.username,
             'friends': self.user.username})
        self.assertEqual(response.status_code, 200)
        friend = User.objects.get(username__exact='test0')
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem1', 'amount': 100, 'paid_user': self.user,
             'friends': friend.username})
        "verifying creating transaction objects"
        transactions = Friendship.objects.get(
            user=friend, friend=self.user).transactions.all()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(len(Transaction.objects.all()), 2)
        self.assertEqual(transactions[0].amount, 100)
        self.assertEqual(transactions[0].owe_id, friend.id)
        self.assertEqual(transactions[0].item, 'testitem1')
        transactions = Friendship.objects.get(
            user=self.user, friend=friend).transactions.all()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].amount, 100)
        self.assertEqual(transactions[0].owe_id, friend.id)
        self.assertEqual(transactions[0].item, 'testitem1')
        "verifying another post"
        new_friend = User.objects.get(username__exact='test1')
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 12, 'paid_user': self.user.username,
             'friends': [self.user.username, friend.username,
                         new_friend.username]})
        transactions = Friendship.objects.get(
            user=self.user, friend=new_friend).transactions.all()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].amount, 4)
        self.assertEqual(transactions[0].owe_id, new_friend.id)
        self.assertEqual(transactions[0].item, 'testitem')
        transactions = Friendship.objects.get(
            user=new_friend, friend=self.user).transactions.all()
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0].amount, 4)
        self.assertEqual(transactions[0].owe_id, new_friend.id)
        self.assertEqual(transactions[0].item, 'testitem')
        self.assertEqual(response.status_code, 302)
        other_friend = User.objects.get(username__exact='test1')
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'item', 'amount': 20, 'paid_user': self.user.username,
             'friends': [self.user.username, other_friend.username]})
        self.assertEqual(response.status_code, 302)
        transactions = Friendship.objects.get(
            user=self.user, friend=other_friend).transactions.all()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[1].amount, 10)
        self.assertEqual(transactions[1].owe_id, other_friend.id)
        self.assertEqual(transactions[1].item, 'item')
        transactions = Friendship.objects.get(
            user=other_friend, friend=self.user).transactions.all()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(response.status_code, 302)
        friend = User.objects.get(username='test0')
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 100,
             'paid_user': self.user.username,
             'friends': [self.user.username, friend.username]})
        self.assertEqual(response.status_code, 302)
        friendship = Friendship.objects.get(user=self.user, friend=friend)
        reverse_friendsip = Friendship.objects.get(user=friend,
                                                   friend=self.user)
        self.assertEqual(friendship.net_amount, 154)
        self.assertEqual(friendship.owe, friend.id)
        self.assertEqual(reverse_friendsip.net_amount, 154)
        self.assertEqual(reverse_friendsip.owe, friend.id)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 500, 'paid_user': friend.username,
             'friends': [self.user.username, friend.username]})
        self.assertEqual(response.status_code, 302)
        friendship = Friendship.objects.get(user=self.user, friend=friend)
        reverse_friendsip = Friendship.objects.get(
            user=friend, friend=self.user)
        self.assertEqual(friendship.net_amount, 96)
        self.assertEqual(friendship.owe, self.user.id)
        self.assertEqual(friendship.net_amount, 96)
        self.assertEqual(friendship.owe, self.user.id)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'testitem', 'amount': 8, 'paid_user': friend.username,
             'friends': [self.user.username, friend.username]})
        friendship = Friendship.objects.get(user=self.user, friend=friend)
        reverse_friendship = Friendship.objects.get(user=friend,
                                                    friend=self.user)
        self.assertEqual(friendship.net_amount, 100)
        self.assertEqual(friendship.owe, self.user.id)
        self.assertEqual(reverse_friendship.owe, self.user.id)
        self.assertEqual(reverse_friendship.net_amount, 100)
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'item', 'amount': 50, 'paid_user':  self.user.username,
             'friends': [self.user.username, friend.username]})
        friendship = Friendship.objects.get(user=self.user, friend=friend)
        reverse_friendship = Friendship.objects.get(user=friend,
                                                    friend=self.user)
        self.assertEqual(friendship.net_amount, 75)
        self.assertEqual(friendship.owe, self.user.id)
        self.assertEqual(reverse_friendship.net_amount, 75)
        self.assertEqual(reverse_friendship.owe, self.user.id)
        new_friend = User.objects.get(username='test1')
        response = self.c.post(reverse(
            'debt_split_amount'),
            {'item': 'item', 'amount': 60, 'paid_user': new_friend.username,
             'friends': [self.user.username, new_friend.username,
                         friend.username]})
        self.assertEqual(response.status_code, 302)
        friendship_1 = Friendship.objects.get(user=self.user,
                                              friend=new_friend)
        self.assertEqual(friendship_1.owe, self.user.id)
        self.assertEqual(friendship_1.net_amount, 6)
        reverse_friendship_1 = Friendship.objects.get(user=new_friend,
                                                      friend=self.user)
        self.assertEqual(reverse_friendship_1.owe, self.user.id)
        self.assertEqual(reverse_friendship_1.net_amount, 6)
        friendship_2 = Friendship.objects.get(user=new_friend,
                                              friend=friend)
        reverse_friendship_2 = Friendship.objects.get(user=friend,
                                                      friend=new_friend)
        self.assertEqual(friendship_2.owe, friend.id)
        self.assertEqual(friendship_2.net_amount, 20)
        self.assertEqual(reverse_friendship_2.owe, friend.id)
        self.assertEqual(reverse_friendship_2.net_amount, 20)
        friendship_3 = Friendship.objects.get(user=self.user, friend=friend)
        self.assertEqual(friendship_3.owe, self.user.id)
        self.assertEqual(friendship_3.net_amount, 75)
        reverse_friendship_3 = Friendship.objects.get(friend=friend,
                                                      user=self.user)
        self.assertEqual(reverse_friendship_3.owe, self.user.id)
        self.assertEqual(reverse_friendship_3.net_amount, 75)

    def test_for_user_history_view(self):
        num_friends = 10
        "creating users and friends"
        for num in range(num_friends):
            new_user = User.objects.create(username="temporary"+str(num),
                                           password='testpassword')
            Friendship.objects.create(user=self.user, friend=new_user)
            Friendship.objects.create(user=new_user, friend=self.user)
        self.assertEqual(User.objects.count(), 12)
        self.assertEqual(Friendship.objects.count(), 20)
        response = self.c.get(reverse(
            'debt_user_history', kwargs={'username': self.user.username}))
        response = self.c.get(reverse(
            'debt_user_history', kwargs={'username': 'invaliduser'}))
        self.assertEqual(response.status_code, 404)

    def test_for_user_debt_details(self):
        response = self.c.get(reverse('user_net_bill'))
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse('user_net_bill'))
        self.assertEqual(response.status_code, 200)

    def test_user_image(self):
        response = self.c.get(reverse(
            'debt_user_image', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 302)
        self.c.login(username='temporary', password='temporary')
        response = self.c.get(reverse(
            'debt_user_image', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        response = self.c.post(reverse(
            'debt_user_image',
            kwargs={'username': self.user.username}),
            {'image': get_temporary_image})
        self.assertEqual(response.status_code, 302)


def get_temporary_image():
    io = StringIO.StringIO()
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='JPEG')
    image_file = InMemoryUploadedFile(
        io, None, 'foo.jpg', 'jpeg', io.len, None)
    image_file.seek(0)
    return image_file
