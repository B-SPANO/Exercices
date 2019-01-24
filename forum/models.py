from django.db.models import (
    Model, CharField, ManyToManyField, IntegerField,
    ForeignKey, TextField, DateTimeField, PROTECT,
    Manager, BooleanField, OneToOneField, CASCADE,
    )
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth.models import Permission


class ProfileManager(Manager):
    use_for_related_fields = True
    
    def get_queryset(self):
        qs = super(ProfileManager, self).get_queryset()
        return qs


class Profile(Model):
    """ User representation """

    user = OneToOneField(User, related_name='forum_profile', verbose_name=_('User'),on_delete=PROTECT)
    location = CharField(_('Location'), max_length=30, blank=True)
    post_count = IntegerField(_('Post count'), blank=True, default=0)

    objects = ProfileManager()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def last_post(self):
        """ return last post id for the current user """
        posts = Post.objects.filter(profile__id=self.profile_id).order_by('-created')
        if posts:
            return posts[0].created
        else:
            return None

    def __str__(self):
        return str(self.user)

    # def __repr__(self):
    #     return 


class Forum(Model):
    """ Global container """

    name = CharField(_('Name'), max_length=80)
    description = TextField(_('Description'), blank=True, default='')
    moderators = ManyToManyField(User, blank=True, verbose_name=_('Moderators'))
    post_count = IntegerField(_('Post count'), blank=True, default=0)
    topic_count = IntegerField(_('Topic count'), blank=True, default=0)
    last_post = ForeignKey('Post', related_name='last_forum_post',on_delete=PROTECT, blank=True, null=True)

    class Meta:
        verbose_name = _('Forum')
        verbose_name_plural = _('Forums')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('current_app:forum', args=[self.id])
    
    @property
    def posts(self):
        """ create left-join between Posts and Forum """
        return Post.objects.filter(topic__forum__id=self.id).select_related()
    

class Topic(Model):
    """ Subject thread """

    forum = ForeignKey(Forum, related_name='topics', verbose_name=_('Forum'), on_delete=PROTECT)
    name = CharField(_('Subject'), max_length=255)
    created = DateTimeField(_('Created'),auto_now_add=True)
    profile = ForeignKey(Profile, verbose_name=_('User'), on_delete=PROTECT)
    closed = BooleanField(_('Closed'), blank=True, default=False)
    post_count = IntegerField(_('Post count'), blank=True, default=0)
    last_post = ForeignKey('Post', related_name='last_topic_post', blank=True, null=True, on_delete=PROTECT)
    # subscribers = ManyToManyField(Profile, related_name='subscriptions', through='Subscrition' , blank=True)

    class Meta:
        ordering = ['-created']
        get_latest_by = 'created'
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('forum:topic', args=[self.id])

    def delete(self, *arg, **kwargs):
        """ 
        Overloading Delete method.
        Topic can be deleted, only if cannot contains Posts
        """
        try:
            if self.post_count == 0:
                super().delete()
        except PermissionDenied:
            return "This subject isn't empty and cannot be deleted"
    
    # @property
    # def reply_count(self):
    #     return self.post_count - 1


class Post(Model):
    """ Unitary message """

    topic = ForeignKey(Topic, related_name='posts', on_delete=PROTECT, verbose_name=_('Topics'))
    profile = ForeignKey(Profile, related_name='posts', on_delete=PROTECT, verbose_name=_('User'))
    created = DateTimeField(_('Created'), auto_now_add=True)
    updated = DateTimeField(_('Updated'), blank=True, null=True)
    updated_by = ForeignKey(User, verbose_name=_('Updated by'), on_delete=PROTECT, blank=True, null=True)
    body = TextField(_('Message'))

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('forum:post', args=[self.id])

    def delete(self, *arg, **kwargs):
        super(Post, self).delete()
    
    def summary(self):
        """
        Create a post summary for a better 
        representation on list views
        """
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or ''
        return self.body[:LIMIT] + tail

    def __str__(self):
        return self.summary()


class Subscription(Model):
    """ Subscription on topics for mailling news messages  """
    
    topic = ForeignKey(Topic, on_delete=CASCADE, related_name="topic_subscribed")
    profile = ForeignKey(Profile, on_delete=CASCADE)
    value = BooleanField(default=False)


# class PostTracking(models.Model): TODO: need to be implemented... (one day maybe...)
#     """
#     Model for tracking read/unread posts.
#     In topics stored ids of topics and last_posts as dict.
#     """

#     user = OneToOneField(User)
#     topics = JSONField(null=True, blank=True)
#     last_read = models.DateTimeField(null=True, blank=True)

#     class Meta:
#         verbose_name = _('Post tracking')
#         verbose_name_plural = _('Post tracking')

#     def __str__(self):
#         return self.user.username