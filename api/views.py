from django.http import JsonResponse
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def my_view(request):
    return HttpResponse("Hello, World!")


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/user',
    ]

    return Response(routes)
