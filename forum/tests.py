import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from forum import factories
from forum.models import Profile, Forum


class ProfileCreationTestCase(unittest.TestCase):

    def test_creation(self):
        user = User.objects.create(
            username="Toto", password="qwertyu123456"
            )
        Profile.objects.create(user=user, location="Lunel")
        self.assertTrue(
            Profile.objects.filter(user=user).exists()
        )
        self.assertTrue(
            Profile.objects.filter(user__username="Toto").exists()
        )
class ProfileTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass
        user = User.objects.create(
            username="Tutu", password="qwertyu123456"
            )
        cls.profile = Profile.objects.create(user=user, location="Lunel")

    def test_location(self):
        self.assertEqual(self.profile.location, "Lunel")

    def test_post_count(self):
        self.assertEqual(self.profile.post_count, 0)


    def test_location2(self):
        self.assertEqual(Profile.objects.get(user__username="Tutu").location, "Lunel")

    def test_post_count2(self):
        self.assertEqual(Profile.objects.first().post_count, 0)


class ForumCreationTestCase(unittest.TestCase):

    def test_creation(self):
        forum = factories.ForumFactory()
        self.assertIn(Forum.objects.filter(pk=self.name), forum.name)


class ForumTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        super().setUpClass
        cls.forum = factories.ForumFactory()

    def test_description(self):
        self.assertIn(Forum.objects.filter(pk=self.description), forum.description)


#TODO: trouver le Assert valide et suffisament specifique, car a 
# chaque reload des tests les valeur generees incrementent
