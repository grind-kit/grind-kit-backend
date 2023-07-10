from django.test import TestCase
from firebase_admin import auth
from decouple import config


class ConditionsEndpointTest(TestCase):
    def test_get_conditions_success(self):
        query_params = {
            'type': '4',
            'min': '50',
            'max': '60'
        }

        response = self.client.get('/api/conditions/', data=query_params)
        print(response.json())
        
        self.assertEqual(response.status_code, 200)
