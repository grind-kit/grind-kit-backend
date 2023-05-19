from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirebaseUser as User
from .models import ContentFinderCondition, InstanceContentBookmark
from .serializers import FirebaseUserSerializer as UserSerializer
from .serializers import ContentFinderConditionSerializer, InstanceContentBookmarkSerializer
from django.core.cache import cache
from .ratelimit import RateLimit, RateLimitSucceeded
from django.utils import timezone


@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(
            username=username, email=email, password=password)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def user_info_view(request, username: str):
    if not username:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f'uid_{username}'

    cached_response = cache.get(cache_key)

    if cached_response and request.method == 'GET':
        return Response(cached_response, status=status.HTTP_200_OK)

    try:
        RateLimit(
            key=f"uid_{username}",
            limit=10,
            period=60
        ).check()
    except RateLimitSucceeded as e:
        return Response(
            f"Rate limit exceeded. You have used {e.usage} of {e.limit} requests in the last minute.",
            status=429
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_content_finder_conditions(request):
    type_id = request.GET.get('type')
    min_level = request.GET.get('min')
    max_level = request.GET.get('max')
    cache_key = f'content_finder_conditions_{type_id}_{min_level}_{max_level}'

    cached_response = cache.get(cache_key)

    if cached_response:
        return Response(cached_response, status=status.HTTP_200_OK)

    if not min_level or not max_level:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    conditions = ContentFinderCondition.objects.filter(
        class_job_level_required__gte=min_level,
        class_job_level_required__lte=max_level,
        content_type_id=type_id
    )
    serializer = ContentFinderConditionSerializer(conditions, many=True)

    if not serializer.data:
        return Response({'error': 'No matching conditions found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.data, status=status.HTTP_200_OK)


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

    elif request.method == 'POST':

        content_finder_condition_id = request.data.get(
            'content_finder_condition')
        content_finder_condition = ContentFinderCondition.objects.get(
            id=content_finder_condition_id)
        content_type_id = request.data.get('content_type_id')
        created = timezone.now()

        if not content_type_id or not content_finder_condition_id:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        if InstanceContentBookmark.objects.filter(user=user, content_finder_condition=content_finder_condition_id).exists():
            return Response({'error': 'Bookmark already exists'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bookmark = InstanceContentBookmark.objects.create(
                user=user,
                content_finder_condition=content_finder_condition,
                content_type_id=content_type_id,
                value=1,
                created=created
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = InstanceContentBookmarkSerializer(bookmark)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/users',
        '/api/users/<str:username>',
        '/api/users/<int:user_id>/bookmarks',
        '/api/conditions',
    ]

    return Response(routes)
