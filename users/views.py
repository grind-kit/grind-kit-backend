from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FirebaseUser, FirebaseUserToken, UserBookmark
from .serializers import FirebaseUserSerializer, FirebaseUserTokenSerializer, UserBookmarkGetSerializer, UserBookmarkUpdateSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404
from decouple import config
import requests


class UserProfileRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get(self, request, pk):
        queryset = self.get_queryset(pk)
        serializer = self.get_serializer(queryset)

        return Response(serializer.data)

    def patch(self, request, pk):
        queryset = self.get_queryset(pk)
        serializer = self.get_serializer(
            queryset, data=request.data, partial=True)

        if serializer.is_valid():
            updated_at = timezone.now()
            serializer.validated_data['updated_at'] = updated_at

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self, pk):
        queryset = get_object_or_404(FirebaseUser, pk=pk)
        return queryset

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class UserCreate(generics.CreateAPIView):
    serializer_class = FirebaseUserSerializer

    def create(self, request, *args, **kwargs):

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        id_token = request.data.get('idToken')
        refresh_token = request.data.get('refreshToken')

        if not username or not email or not password or not id_token:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Create user token
        token_data = {
            'user': user.id,
            'id_token': id_token,
            'refresh_token': refresh_token
        }

        token_serializer = FirebaseUserTokenSerializer(data=token_data)
        token_serializer.is_valid(raise_exception=True)
        token_serializer.save()

        # Return a response
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class UserTokenRefresh(APIView):
    def refresh_id_token(self, request):
        # Check if request is POST
        if request.method != 'POST':
            return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        # Get username
        username = request.data.get('username')

        # Check if username is present
        if not username:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user
        try:
            user = FirebaseUser.objects.get(username=username)
        except FirebaseUser.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Get user token
        try:
            user_token = FirebaseUserToken.objects.get(user=user)
        except FirebaseUserToken.DoesNotExist:
            return Response({'error': 'User token does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get refresh token
        refresh_token = user_token.refresh_token

        # Firebase settings
        firebase_api_key = config('FIREBASE_API_KEY')
        refresh_url = f'https://securetoken.googleapis.com/v1/token?key={firebase_api_key}'
        refresh_payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        try:
            response = requests.post(refresh_url, data=refresh_payload)
            response_data = response.json()

            if 'id_token' in response_data:

                # Update user token using new token
                serializer = self.get_serializer(
                    user_token, data={'id_token': response_data['id_token']}, partial=True)

                if serializer.is_valid():
                    updated_at = timezone.now()
                    serializer.validated_data['updated_at'] = updated_at

                    serializer.save(user=user_token)
                    return Response({'id_token': response['id_token']}, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        # Check if request is POST
        if request.method != 'POST':
            return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        username = request.data.get('username')
        id_token = request.data.get('id_token')
        refresh_token = request.data.get('refresh_token')

        # Check if required data is present
        if not username or not id_token or not refresh_token:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        # Get user for OneToOneField
        firebase_user = FirebaseUser.objects.get(username=username)

        firebase_user_token, created = FirebaseUserToken.objects.get_or_create(
            user=firebase_user,
            defaults={
                'id_token': id_token,
                'refresh_token': refresh_token,
                'updated_at': timezone.now()
            }
        )

        if not created:
            firebase_user_token.id_token = id_token
            firebase_user_token.refresh_token = refresh_token
            firebase_user_token.save()

        # Return user token
        serializer = FirebaseUserTokenSerializer(firebase_user_token)
        return Response(serializer.data, status=status.HTTP_200_OK)

# User Bookmarks


class UserBookmarkListCreate(generics.ListCreateAPIView):
    serializer_class = UserBookmarkGetSerializer

    def list(self, request, user_id, *args, **kwargs):
        queryset = self.get_queryset(user_id)
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @staticmethod
    def get_queryset(user_id):
        queryset = UserBookmark.objects.filter(user_id=user_id)
        return queryset

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class UserBookmarkRetrieveUpdate(generics.RetrieveUpdateAPIView):

    def get(self, request, user_id, bookmark_id, *args, **kwargs):
        queryset = self.get_queryset(user_id, bookmark_id)
        serializer = self.get_serializer(queryset)

        return Response(serializer.data)

    def patch(self, request, user_id, bookmark_id, *args, **kwargs):
        queryset = self.get_queryset(user_id, bookmark_id)
        serializer = self.get_serializer(
            queryset, data=request.data, partial=True)

        if serializer.is_valid():
            updated_at = timezone.now()
            serializer.validated_data['updated_at'] = updated_at

            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self, user_id, bookmark_id):
        queryset = UserBookmark.objects.get(user_id=user_id, id=bookmark_id)

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            return UserBookmarkGetSerializer(*args, **kwargs)
        elif self.request.method == 'PATCH':
            return UserBookmarkUpdateSerializer(*args, **kwargs)


@api_view(['GET'])
def get_routes(request):
    routes = [
        '<int:user_id>/bookmarks/',
        '<int:user_id>/bookmarks/<int:bookmark_id>',
        '<int:pk>/',
        'auth/signup/',
        'auth/login/',
    ]

    return Response(routes)
