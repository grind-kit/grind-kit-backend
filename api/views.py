from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirebaseUser as User
from .models import ContentFinderCondition
from .serializers import FirebaseUserSerializer as UserSerializer
from .serializers import ContentFinderConditionSerializer
from django.core.cache import cache


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

@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/users',
        '/api/users/<str:username>',
        '/api/conditions',
    ]

    return Response(routes)
