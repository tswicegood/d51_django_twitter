from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from d51_django_twitter.models import TwitterUser, Relationship
import twitterro
import random
import mox

def replay_all(*args):
    [mox.Replay(obj) for obj in args]

def verify_all(*args):
    [mox.Verify(obj) for obj in args]

def tswicegood_user():
    """
    Builds a UserRemoteObject that looks like tswicegood was at one point
    """
    user = twitterro.remote_objects.UserRemoteObject()
    user.update_from_dict(
        {'created_at': 'Tue Oct 16 14:55:08 +0000 2007',
         'description': 'One of a dozen people in American that can sight-read 837* forms~',
         'favourites_count': 455,
         'followers_count': 601,
         'following': False,
         'friends_count': 227,
         'geo_enabled': False,
         'id': 9478892,
         'location': 'Lawrence, KS',
         'name': 'Travis Swicegood',
         'notifications': False,
         'profile_background_color': '000000',
         'profile_background_image_url': 'http://a1.twimg.com/profile_background_images/2861802/gitbook.jpg',
         'profile_background_tile': False,
         'profile_image_url': 'http://a1.twimg.com/profile_images/406377310/me-square_normal.jpg',
         'profile_link_color': '3DA0A5',
         'profile_sidebar_border_color': '1C1C1C',
         'profile_sidebar_fill_color': '676767',
         'profile_text_color': '000000',
         'protected': False,
         'screen_name': 'tswicegood',
         'status': {'created_at': 'Mon Oct 12 19:26:40 +0000 2009',
                    'favorited': False,
                    'geo': None,
                    'id': 4815319977L,
                    'in_reply_to_screen_name': 'Bagyants',
                    'in_reply_to_status_id': 4814291446L,
                    'in_reply_to_user_id': 19638752,
                    'source': '<a href="http://www.atebits.com/" rel="nofollow">Tweetie</a>',
                    'text': "@Bagyants That explains it.  I haven't hit the gym in awhile and haven't been on my bike nearly enough! :-D",
                    'truncated': False},
         'statuses_count': 4512,
         'time_zone': 'Tehran',
         'url': 'http://www.travisswicegood.com',
         'utc_offset': 12600,
         'verified': False}
    )
    user._delivered = True
    return user

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

    def test_can_update_from_twitter(self):
        tswicegood = tswicegood_user()
        twitter = mox.MockObject(twitterro.Twitter)
        twitter.users = mox.MockObject(twitterro.User)
        twitter.users.show(screen_name = "tswicegood").AndReturn(tswicegood)
        replay_all(twitter, twitter.users)

        user = TwitterUser(screen_name = 'tswicegood')
        user.update_from_twitter(twitter = twitter)
        self.assertEqual(user.screen_name, tswicegood.screen_name)
        self.assertEqual(user.id, tswicegood.id)

