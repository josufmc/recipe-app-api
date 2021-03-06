from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicTagsApiTest(TestCase):
    """ Tests publicly available tags from API """

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ Test that login is required for retrieving tags """
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """ Tests authorized tags from API"""

    def setUp(self):
        user_vals = {
            'email': 'test@example.com',
            'password': 'testpass',
            'name': 'Test Name',
        }
        self.user = create_user(**user_vals)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """ Test retrieving tags """
        Tag.objects.create(
            user=self.user,
            name='Vegan'
        )
        Tag.objects.create(
            user=self.user,
            name='Dessert'
        )

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """ Test that tags returned are for the authenticated user """
        user_vals = {
            'email': 'other@example.com',
            'password': 'otherpass',
            'name': 'Other Name',
        }
        user2 = create_user(**user_vals)
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Confort Food')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """" Test creating a new tag """
        payload = {
            'name': 'Test Tag',
        }
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """ Test creating new tag with invalid name """
        payload = {
            'name': '',
        }
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
