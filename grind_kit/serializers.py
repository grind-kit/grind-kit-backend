from rest_framework.serializers import ModelSerializer
from . models import *

class InstanceContentSerializer(ModelSerializer):
    class Meta:
        model = InstanceContent
        fields = '__all__'