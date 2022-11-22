from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializers import *

@api_view(['GET'])
def getRoutes (request):
    routes = [
        {
            'Endpoint': '/instancecontent',
            'method': 'GET',
            'description': 'Returns an array of instance content'
        },
    ]

    return Response(routes)

@api_view(['GET'])
def getInstanceContent (request):
    content = InstanceContent.objects.all()
    serializer = InstanceContentSerializer(content, many=True)
    return Response(serializer.data)
