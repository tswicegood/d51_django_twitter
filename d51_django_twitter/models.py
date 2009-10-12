from django.db import models

class TwitterUser(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200, null=True)
    screen_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=140, null=True)
    url = models.URLField(max_length=250, null=True)
    friends_count = models.IntegerField(default=0)
    statuses_count = models.IntegerField(default=0)
    followers_count = models.IntegerField(default=0)
    favourites_count = models.IntegerField(default=0)
    protected = models.BooleanField()
    profile_image_url = models.CharField(max_length=500, null=True)
    profile_background_color = models.CharField(max_length=8, null=True)
    profile_background_image_url = models.URLField(null=True)
    profile_background_tile = models.BooleanField()
    profile_link_color = models.CharField(max_length=8, null=True)
    profile_text_color = models.CharField(max_length=8, null=True)
    profile_sidebar_fill_color = models.CharField(max_length=8, null=True)
    profile_sidebar_border_color = models.CharField(max_length=8, null=True)
    created_at = models.DateTimeField(null=True)
    utc_offset = models.IntegerField(null=True)
    time_zone = models.CharField(max_length = 50, null=True)

    internal_last_updated = models.DateTimeField(auto_now=True)

    def get_followers(self):
        return TwitterUser.objects.filter(following_relationships__target = self)
    followers = property(get_followers)

    def get_following(self):
        return TwitterUser.objects.filter(follower_relationships__source = self)
    following = property(get_following)

    def follow(self, user):
        return Relationship.objects.create(source=self, target=user)

    def __unicode__(self):
        return "%s [%s]" % (self.screen_name, self.id)

class Relationship(models.Model):
    source = models.ForeignKey(TwitterUser, related_name='following_relationships')
    target = models.ForeignKey(TwitterUser, related_name='follower_relationships')

    def __unicode__(self):
        return "%s following %s" % (self.source, self.target)



