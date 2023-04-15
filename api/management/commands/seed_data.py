import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

import requests
from django.core.management.base import BaseCommand
from decouple import config
from api.models import ContentFinderCondition


class Command(BaseCommand):
    help = 'Seeds the database with ContentFinderCondition data'

    def handle(self, *args, **options):
        # Define the base URL for the XIVAPI endpoint
        base_url = config('XIVAPI_URL') + 'ContentFinderCondition/'

        # Loop through pages 1-10 to retrieve all data
        for page in range(1, 11):
            # Define the query parameters for the API request
            params = {
                'language': 'en',
                'columns': 'ID,Name,ClassJobLevelRequired,ItemLevelRequired,Url,ContentType.ID,AcceptClassJobCategory',
                'page': page,
                'private_key': config('XIVAPI_KEY'),
            }

            # Make the API request
            response = requests.get(base_url, params=params)
            response_data = response.json()

            # Loop through the data and save it to the database
            for content in response_data['Results']:
                # Create a new ContentFinderCondition object
                new_content = ContentFinderCondition(
                    id=content['ID'],
                    name=content['Name'],
                    class_job_level_required=content['ClassJobLevelRequired'],
                    item_level_required=content['ItemLevelRequired'],
                    url=content['Url'],
                    content_type_id=content['ContentType']['ID'],
                    accept_class_job_category=content['AcceptClassJobCategory'],
                )
                new_content.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully seeded ContentFinderCondition data'))
