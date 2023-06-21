from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FirebaseUser, FirebaseUserToken, UserBookmark
from .serializers import FirebaseUserSerializer, FirebaseUserTokenSerializer, UserBookmarkSerializer


class UserCreate(generics.CreateAPIView):
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


class UserBookmarkCreate(generics.CreateAPIView):
    queryset = UserBookmark.objects.all()
    serializer_class = UserBookmarkSerializer

    def create(self, request, *args, **kwargs):
        # Check if request is POST
        if request.method != 'POST':
            return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user_id = request.data.get('user_id')
        content_finder_condition_id = request.data.get(
            'content_finder_condition_id')
        content_type_id = request.data.get('content_type_id')

        if not user_id or not content_finder_condition_id or not content_type_id:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)


@api_view(['PATCH'])
def patch_bookmark_view(request, user_id: int, bookmark_id: int):
    if request.method not in ['PATCH']:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if not user_id or not bookmark_id:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        bookmark = InstanceContentBookmark.objects.get(id=bookmark_id)

        if not bookmark:
            return Response({'error': 'Bookmark not found'}, status=status.HTTP_404_NOT_FOUND)

        bookmark.value = request.data.get('value')
        bookmark.save()

        serializer = InstanceContentBookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user_bookmark_view(request, user_id: int):

    if request.method not in ['GET', 'POST']:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if not user_id:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.get(id=user_id)

    if request.method == 'GET':
        try:
            bookmarks = InstanceContentBookmark.objects.filter(user=user)

            if not bookmarks:
                return Response({'error': 'No bookmarks found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InstanceContentBookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_routes(request):
    routes = [
        '<int:user_id>/bookmarks/',
        'users/<int:user_id>/bookmarks/<int:bookmark_id>',
    ]

    return Response(routes)
