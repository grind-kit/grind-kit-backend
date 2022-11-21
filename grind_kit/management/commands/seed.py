import requests
from django.core.management.base import BaseCommand
from ...models import InstanceContent

def get_content():
    url = 'https://xivapi.com/InstanceContent'
    response = requests.get(url)
    data = response.json()
    content = data['Results']
    return content

def clear_data():
    InstanceContent.objects.all().delete()

def seed_content():
    for i in get_content():
        all_content = InstanceContent(
            id = i['ID'],
            name = i['Name'],
            url = i['Url']
        )
        all_content.save()

class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
        seed_content()
        print("completed")