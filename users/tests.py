from django.test import TestCase
from users.models import FirebaseUser


class BookmarksEndpointTest(TestCase):
    fixtures = ['users/fixtures/bookmarks.json']

    def test_get_bookmarks_success(self):
        user_id = 1

        response = self.client.get(f'users/{user_id}/bookmarks/')

        # Status code should be 200
        self.assertEqual(response.status_code, 200)
