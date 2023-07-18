from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import FirebaseUser, UserBookmark
from api.models import ContentFinderCondition
from rest_framework import status


class BookmarksEndpointTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_bookmark(self):
        test_user = FirebaseUser.objects.create_user(
            username='John Doe',
            email='john_doe@gmail.com',
        )

        test_content_finder_condition = ContentFinderCondition.objects.create(
            id=1,
            name='Test Content Finder Condition',
            class_job_level_required=123,
            item_level_required=456,
            url='https://www.google.com',
            content_type_id=789,
            accept_class_job_category={'WAR': '123'},
        )

        url = reverse('list-create-bookmark', kwargs={'user_id': test_user.id})

        data = {
            'user_id': test_user.id,
            'content_finder_condition_id': test_content_finder_condition.id,
            'content_type_id': 789,
        }

        response = self.client.post(url, data, format='json')

        # Check that we return a 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that a UserBookmark was created, and that it has the correct user_id
        self.assertEqual(UserBookmark.objects.count(), 1)
        self.assertEqual(UserBookmark.objects.first().user_id, test_user)

    def tearDown(self):
        pass
