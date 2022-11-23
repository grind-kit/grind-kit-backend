from django.shortcuts import render
from rest_framework.parsers import JSONParser 
from rest_framework import status
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

@api_view(['GET', 'POST'])
def jobList (request):
    if request.method == 'GET':
        job = Job.objects.all()
        serializer = JobSerializer(job, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        job_data = JSONParser().parse(request)
        serializer = JobSerializer(data=job_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # if request.method == 'GET':
    #     job_data = Job.objects.filter(id=pk)
    #     serializer = JobSerializer(job_data, many=True)
    #     return Response(serializer.data)