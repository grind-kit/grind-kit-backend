import time
from django.http import JsonResponse
from firebase_admin import auth
from decouple import config


class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        path_info = request.META.get('PATH_INFO')

        if path_info.startswith('/api/users'):
            # Allow access to user creation without Firebase token
            response = self.get_response(request)
            return response

        if path_info.startswith('/admin/'):
            # Allow access to admin without Firebase token
            response = self.get_response(request)
            return response

        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

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
            return JsonResponse({'error': str(e)}, status=401)

        response = self.get_response(request)
        return response
