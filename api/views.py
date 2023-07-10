from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import ContentFinderCondition
from .serializers import ContentFinderConditionSerializer
from django.core.cache import cache


class ContentFinderConditionList(generics.ListAPIView):
    serializer_class = ContentFinderConditionSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ContentFinderConditionSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        type_id = self.request.query_params.get('type')
        min_level = self.request.query_params.get('min')
        max_level = self.request.query_params.get('max')
        cache_key = f'content_finder_conditions_{type_id}_{min_level}_{max_level}'
        cached_response = cache.get(cache_key)

        if cached_response:
            return cached_response

        if not min_level or not max_level:
            return ContentFinderCondition.objects.none()

        return ContentFinderCondition.objects.filter(
            class_job_level_required__gte=min_level,
            class_job_level_required__lte=max_level,
            content_type_id=type_id
        )

@api_view(['GET'])
def get_routes(request):
    routes = [
        'conditions/',
    ]

    return Response(routes)
