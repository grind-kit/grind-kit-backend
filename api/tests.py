from django.test import TestCase


class ConditionsEndpointTest(TestCase):
    fixtures = ['api/fixtures/conditions.json']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_conditions_success(self):
        query_params = {
            'type': '8',
            'min': '50',
            'max': '60'
        }

        response = self.client.get('/api/conditions/', data=query_params)

        # Status code should be 200
        self.assertEqual(response.status_code, 200)

        # Response should be a list of 2 conditions
        conditions = response.data
        self.assertEqual(len(conditions), 2)

        # Check that the conditions are the correct ones
        for condition in conditions:
            self.assertEqual(condition['content_type_id'], 8)
            self.assertGreaterEqual(condition['class_job_level_required'], 50)
            self.assertLessEqual(condition['class_job_level_required'], 60)
