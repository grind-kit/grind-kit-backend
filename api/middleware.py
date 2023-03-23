from django.http import JsonResponse
from firebase_admin import auth


class FirebaseAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return JsonResponse({'error': 'Authorization header missing'}, status=401)

        try:
            id_token = auth_header.split(' ').pop()
            decoded_token = auth.verify_id_token(id_token)
            request.user_id = decoded_token['uid']
        except:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response
