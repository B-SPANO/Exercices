import factory
from functools import partial
from random import Random
from .models import (
    Profile, Forum, Topic,
    Post, Subscription
    )


Faker = partial(factory.Faker, locale="fr_FR")

class ProfileFactory(factory.django.DjangoModelFactory):
    """
    the factory populate Profile model for
    unit testing.
    """
    class Meta:
        """ setting profile model as reference """
        model = Profile

    user = factory.Faker('name')
    location = factory.Faker('country')
    post_count = factory.Faker('pyint')


class ForumFactory(factory.django.DjangoModelFactory):
    """
    the factory populate Forum model for
    unit testing.
    """
    class Meta:
        """ setting forum model as reference """
        model = Forum

    name = factory.Sequence(lambda k: 'forum%d' % k)
    description = factory.Faker('sentence', nb_words=4)

    # def set_moderators(self, create, extracted, **kwargs):
    #     """ m2m moderators """
    #     self.s
    # # moderators = factory See M2M


class TopicFactory(factory.django.DjangoModelFactory):
    """
    the factory populate Topic model for
    unit testing.
    """
    class Meta:
        """ setting topic model as reference """
        model = Topic

    forum = factory.SubFactory(ForumFactory)
    profile = factory.SubFactory(ProfileFactory)


class PostFactory(factory.django.DjangoModelFactory):
    """
    the factory populate Post model for
    unit testing.
    """
    class Meta:
        """ setting post model as reference """
        model = Post

    topic = factory.SubFactory(TopicFactory)
    profile = factory.SubFactory(ProfileFactory)
    body = factory.Faker('text')


class SubscriptionFactory(factory.django.DjangoModelFactory):
    """
    the factory populate Subscription model for
    unit testing.
    """
    class Meta:
        """ setting post model as reference """
        model = Subscription

    topic = factory.SubFactory(TopicFactory)
    profile = factory.SubFactory(ProfileFactory)
    value = factory.Faker('boolean')
    