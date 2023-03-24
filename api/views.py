from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


@api_view(['POST'])
def create_user(request):
    uid = request.data.get('uid')
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.create_user(uid=uid, email=email, password=password)
    user.save()

    return Response({'message': 'User created successfully'})


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/user',
    ]

    return Response(routes)
