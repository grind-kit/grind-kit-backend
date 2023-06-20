from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import FirebaseUser
from .serializers import FirebaseUserSerializer

class FirebaseUserCreate(generics.CreateAPIView):
    queryset = FirebaseUser.objects.all()
    serializer_class = FirebaseUserSerializer

    def create(self, request, *args, **kwargs):
        # Check if request is POST
        if request.method != 'POST':
            return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if required data is present
        if not username or not email or not password:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
                
        # Create user
        return super().create(request, *args, **kwargs)