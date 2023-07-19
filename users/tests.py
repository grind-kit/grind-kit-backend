from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import FirebaseUser, UserBookmark
from api.models import ContentFinderCondition
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.core.management import call_command

class BookmarksEndpointTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        call_command('flush', verbosity=0, interactive=False)

    @classmethod
    def setUpTestData(cls):

        cls.test_user = FirebaseUser.objects.create(
            username='John Doe',
            email='john_doe@gmail.com',
        )

        cls.test_content_finder_condition = ContentFinderCondition.objects.create(
            id=1,
            name='Test Content Finder Condition',
            class_job_level_required=123,
            item_level_required=456,
            url='https://www.google.com',
            content_type_id=789,
            accept_class_job_category={'WAR': '123'},
        )

        cls.test_bookmark = UserBookmark.objects.create(
            user_id=cls.test_user,
            content_finder_condition_id=cls.test_content_finder_condition,
            content_type_id=789,
        )

    # def test_get_user_bookmark(self):
    #     url = reverse("retrieve-update-bookmark",
    #                   kwargs={'user_id': self.test_user.id, 'bookmark_id': self.test_bookmark.id})

    #     response = self.client.get(url, format='json')
    #     print(response.data, "🌯")

    def test_create_user_bookmark(self):

        url = reverse('list-create-bookmark',
                      kwargs={'user_id': self.test_user.id})

        data = {
            'user_id': self.test_user.id,
            'content_finder_condition_id': self.test_content_finder_condition.id,
            'content_type_id': self.test_content_finder_condition.content_type_id,
        }

        response = self.client.post(url, data, format='json')
        print(response.data, "🌯")

        # Check that we return a 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that a UserBookmark was created, and that it has the correct user_id
        self.assertEqual(UserBookmark.objects.count(), 1)
        self.assertEqual(UserBookmark.objects.first().user_id, self.test_user)

    def test_create_user_bookmark_with_invalid_user_id(self):

        # Invalid user_id
        url = reverse('list-create-bookmark', kwargs={'user_id': 999})

        data = {
            'user_id': 999,
            'content_finder_condition_id': self.test_content_finder_condition.id,
            'content_type_id': self.test_content_finder_condition.content_type_id
        }

        response = self.client.post(url, data, format='json')

        # Check that we return a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that we throw an error for the invalid user_id
        expected = {
            'user_id': [ErrorDetail(string='Invalid pk "999" - object does not exist.', code='does_not_exist')]
        }
        self.assertEqual(response.json(), expected)

    def test_create_user_bookmark_with_invalid_content_finder_condition(self):

        url = reverse('list-create-bookmark',
                      kwargs={'user_id': self.test_user.id})

        data = {
            'user_id': self.test_user.id,
            # Invalid content_finder_condition and content_type_id
            'content_finder_condition_id': 999,
            'content_type_id': 999
        }

        response = self.client.post(url, data, format='json')

        expected = {
            'content_finder_condition_id': [ErrorDetail(string='Invalid pk "999" - object does not exist.', code='does_not_exist')]
        }

        # Check that we return a 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that we throw an error for the invalid content_finder_condition_id
        self.assertEqual(response.json(), expected)

    @classmethod
    def tearDownClass(cls):
        # Delete the created objects in reverse order because of foreign key constraints
        cls.test_bookmark.delete()
        cls.test_content_finder_condition.delete()
        cls.test_user.delete()

        super().tearDownClass()
