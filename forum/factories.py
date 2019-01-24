import factory
from random import Random
from models import (
    Profile, Forum, Topic,
    Post, Subscription
    )

# signal user/profile/creation voir doc
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
        
    user = factory.Faker('name')
    location = factory.Faker('country')
    post_count = factory.Faker('pyint')


class ForumFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Forum

    name = factory.Sequence(lambda k: 'forum%d' % k)
    description = factory.Faker('sentence', nb_words=4)
    
    # def set_moderators(self, create, extracted, **kwargs):
    #     """ m2m moderators """
    #     self.s
    # # moderators = factory See M2M


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    forum = factory.SubFactory(ForumFactory)
    profile = factory.SubFactory(ProfileFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    topic = factory.SubFactory(TopicFactory)
    profile = factory.SubFactory(ProfileFactory)
    body = factory.Faker('text')


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    topic = factory.SubFactory(TopicFactory)
    profile = factory.SubFactory(ProfileFactory)
    value = factory.Faker('boolean')