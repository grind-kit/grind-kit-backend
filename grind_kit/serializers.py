from rest_framework.serializers import ModelSerializer
from . models import *

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class InstanceContentSerializer(ModelSerializer):
    class Meta:
        model = InstanceContent
        fields = '__all__'

class JobsSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'