from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import authentication
import firebase_admin.auth as auth


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token["uid"]
        except:
            return None
            
        try:
            user = User.objects.get(username=uid)
            return user

        except ObjectDoesNotExist:
            return None