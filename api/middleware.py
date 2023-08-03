import time
from django.http import JsonResponse
from firebase_admin import auth
from decouple import config
from django.conf import settings
from rest_framework.status import HTTP_401_UNAUTHORIZED

class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.TEST:
            return self.get_response(request)

        auth_header = request.META.get('HTTP_AUTHORIZATION')
        path_info = request.META.get('PATH_INFO')

        # Allow access to admin panel and token refresh endpoint without authentication
        if path_info.startswith('/admin/') or path_info.startswith('/users/auth/token/refresh/'):
            response = self.get_response(request)
            return response

        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=HTTP_401_UNAUTHORIZED)

        try:
            id_token = auth_header.split(' ').pop()
            decoded_token = auth.verify_id_token(id_token)

            # Verify token claims
            if not decoded_token.get('uid'):
                raise ValueError('No UID present in token')

            # Verify token audience
            if decoded_token['aud'] != config('FIREBASE_PROJECT_ID'):
                raise ValueError('Token audience is invalid')

            # Verify token issuer
            if decoded_token['iss'] != 'https://securetoken.google.com/' + config('FIREBASE_PROJECT_ID'):
                raise ValueError('Token issuer is invalid')

            # Verify token expiration time
            if decoded_token['exp'] < time.time():
                raise ValueError('Token has expired')

            request.user_id = decoded_token['uid']
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=HTTP_401_UNAUTHORIZED)

        response = self.get_response(request)
        return response
