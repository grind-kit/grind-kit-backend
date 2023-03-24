from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FirebaseUser as User
from .serializers import FirebaseUserSerializer as UserSerializer

@api_view(['POST'])
def create_user(request):
    uid = request.data.get('uid')
    email = request.data.get('email')
    password = request.data.get('password')

    if not uid or not email or not password:
        return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(uid=uid, email=email, password=password)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def get_routes(request):
    routes = [
        '/api/users',
    ]

    return Response(routes)
