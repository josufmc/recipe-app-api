from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@example.com', password='testpass'):
    """ Create sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ Test creating a new user with an email is successful """
        email = "test@example.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test email for new user is normalized """
        email = "test@EXAMPLE.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        expected_email = "test@example.com"
        self.assertEqual(user.email, expected_email)

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            email = None
            password = "Testpass123"
            get_user_model().objects.create_user(
                email=email,
                password=password
            )

    def test_create_new_superuser_successful(self):
        """ Test creating new superuser """
        email = "test@example.com"
        password = "Testpass123"
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)  # PermissionsMixin
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)
