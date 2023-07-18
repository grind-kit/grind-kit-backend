from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FirebaseUser, FirebaseUserToken, UserBookmark
from .serializers import FirebaseUserSerializer, FirebaseUserTokenSerializer, UserBookmarkGetSerializer, UserBookmarkUpdateSerializer


class UserCreate(generics.CreateAPIView):
    queryset = FirebaseUser.objects.all()
    serializer_class = FirebaseUserSerializer

    def create(self, request, *args, **kwargs):

        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        # Check if required data is present
        if not username or not email or not password:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        return super().create(request, *args, **kwargs)


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

    def get_queryset(self, user_id):
        queryset = UserBookmark.objects.filter(user_id=user_id)
        return queryset

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class UserBookmarkUpdate(generics.RetrieveUpdateAPIView):

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = UserBookmark.objects.filter(user_id=user_id)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserBookmarkGetSerializer
        elif self.request.method == 'PATCH':
            return UserBookmarkUpdateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@api_view(['GET'])
def get_routes(request):
    routes = [
        '<int:user_id>/bookmarks/',
        '<int:user_id>/bookmarks/<int:bookmark_id>',
    ]

    return Response(routes)
