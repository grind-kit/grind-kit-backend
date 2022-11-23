from django.shortcuts import render
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . serializers import *

@api_view(['GET'])
def GetRoutes (request):
    routes = [
        {
            'Endpoint': 'api/instancecontent/',
            'method': 'GET',
            'description': 'Returns an array of all Instance Content'
        },
        {
            'Endpoint': 'api/jobs',
            'method': 'GET',
            'description': "Returns an array of all Accounts' Job Levels"
        },
        {
            'Endpoint': 'api/jobs',
            'method': 'POST',
            'description': "Posts an object for an Account's Job Levels"
        }
    ]

    return Response(routes)

@api_view(['GET'])
def GetInstanceContent (request):
    AllContent = InstanceContent.objects.all()
    Serializer = InstanceContentSerializer(AllContent, many=True)
    return Response(Serializer.data)

@api_view(['GET', 'POST'])
def JobsList (request):
    if request.method == 'GET':
        AllJobs = Job.objects.all()
        Serializer = JobsSerializer(AllJobs, many=True)
        return Response(Serializer.data)
    elif request.method == 'POST':
        JobData = JSONParser().parse(request)
        Serializer = JobsSerializer(data=JobData)
        if Serializer.is_valid():
            Serializer.save()
            return Response(Serializer.data, status=status.HTTP_201_CREATED) 
        return Response(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def JobsDetail (request, pk):
    if request.method == 'GET':
        JobData = Job.objects.filter(id=pk)
        Serializer = JobsSerializer(JobData, many=True)
        return Response(Serializer.data)