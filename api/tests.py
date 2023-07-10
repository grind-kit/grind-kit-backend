from django.test import TestCase
from firebase_admin import auth
from decouple import config

uuid = config('FIREBASE_ADMIN_UUID')
custom_token = auth.create_custom_token(uuid)

class ConditionsEndpointTest(TestCase):
    def test_get_conditions_authenticated(self):
        query_params = {
            'type': '4',
            'min': '1',
            'max': '50'
        }
        headers = {
            'Authorization': f'Bearer {custom_token}'
        }

        response = self.client.get('/api/conditions/', headers=headers, data=query_params)
        print(response.content)
        
        self.assertEqual(response.status_code, 200)
