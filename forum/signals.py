from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from forum.models import Topic, Post


@receiver(post_save, sender=Post, dispatch_uid='forum_post_save')
def post_saved(instance, **kwargs):
    created = kwargs.get('created')
    post = instance
    topic = post.topic

    if created:
        topic.last_post = post
        topic.post_count = topic.posts.count()
        profile = post.user.forum_profile
        profile.post_count = post.user.posts.count()
        profile.save(force_update=True)
    topic.save(force_update=True)


@receiver(post_save, sender=Topic, dispatch_uid='forum_topic_save')
def topic_saved(instance, **kwargs):
    topic = instance
    forum = topic.forum
    forum.topic_count = forum.topics.count()
    forum.post_count = forum.posts.count()
    forum.last_post_id = topic.last_post_id
    forum.save(force_update=True)
