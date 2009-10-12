from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from d51_django_twitter.models import TwitterUser, Relationship
import random

def generate_random_user():
    return TwitterUser(id=str(random.randint(100, 10000)))

def generate_random_users(num):
    return [generate_random_user() for i in range(num)]

class TestOfTwitterUser(TestCase):
    def test_has_followers(self):
        number_of_followers = random.randint(1, 10)
        followers = generate_random_users(number_of_followers)
        user_a = generate_random_user()

        for user in followers:
            user.follow(user_a)

        [u.save() for u in [user_a,] + followers]

        self.assertEqual(user_a.followers.count(), number_of_followers)
        [self.assert_(user in user_a.followers.all()) for user in followers]

    def test_has_following(self):
        number_to_follow = random.randint(1, 10)
        following = generate_random_users(number_to_follow)
        user_a = generate_random_user()

        for user_to_follow in following:
            user_a.follow(user_to_follow)

        [u.save() for u in [user_a,] + following]

        self.assertEqual(user_a.following.count(), number_to_follow)
        [self.assert_(user in user_a.following.all()) for user in following]

