from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from . models import InstanceContent, Job
from . serializers import InstanceContentSerializer, JobsSerializer

from rest_framework.decorators import api_view

@api_view(['GET', 'POST', 'DELETE'])
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
        },
        {
            'Endpoint': 'api/jobs/<int:pk>/',
            'method': 'GET',
            'description': "Returns an object for an Account's Job Levels based on the URL parameter"
        },
        {
            'Endpoint': 'api/jobs/<int:pk>/',
            'method': 'DELETE',
            'description': "Deletes an object for an Account's Job Levels based on the URL parameter"
        },
    ]

    return JsonResponse(routes)

@api_view(['GET'])
def GetInstanceContent (request):
    AllContent = InstanceContent.objects.all()
    Serializer = InstanceContentSerializer(AllContent, many=True)
    return JsonResponse(Serializer.data, safe=False)

@api_view(['GET', 'POST'])
def JobsList (request):
    if request.method == 'GET':
        AllJobs = Job.objects.all()
        Serializer = JobsSerializer(AllJobs, many=True)
        return JsonResponse(Serializer.data, safe=False)
    
    elif request.method == 'POST':
        JobData = JSONParser().parse(request)
        Serializer = JobsSerializer(data=JobData)
        if Serializer.is_valid():
            Serializer.save()
            return JsonResponse(Serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def JobsDetail (request, pk):
    try:
        JobData = Job.objects.filter(id=pk)
    except Job.DoesNotExist:
        return JsonResponse({'message': 'The listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        Serializer = JobsSerializer(JobData, many=True)
        return JsonResponse(Serializer.data, safe=False)
    
    elif request.method == 'PUT':
        ExistingData = Job.objects.get(id=pk)
        NewData = JSONParser().parse(request)
        Serializer = JobsSerializer(ExistingData, data=NewData)
        if Serializer.is_valid():
            Serializer.save()
            return JsonResponse(Serializer.data)
        return JsonResponse(Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        JobData.delete()
        return JsonResponse({'message': 'The listing was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)