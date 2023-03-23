from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["sub"] = settings.SIMPLE_JWT.get("ISSUER", "")
        # When the serializer is called token['exp'] does not reflect the settings.ACCES_TOKEN_LIFETIME
        # and is set to now + 1day,thus we subtract a day to get iat
        token["iat"] = token["exp"] - (60 * 60 * 24)
        # Add additional claims here
        token["claims"] = {"is_superuser": user.is_superuser, "is_staff": user.is_staff}

        return token
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]

    return Response(routes)