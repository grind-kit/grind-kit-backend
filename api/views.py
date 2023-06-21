from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ContentFinderCondition
from .serializers import ContentFinderConditionSerializer
from django.core.cache import cache


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
