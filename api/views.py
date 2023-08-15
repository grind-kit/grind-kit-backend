from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from .models import ContentFinderCondition
from .serializers import ContentFinderConditionSerializer
from users.serializers import UserBookmarkRetrieveSerializer
from django.core.cache import cache
from users.models import UserBookmark


class ContentFinderConditionList(generics.ListAPIView):
    serializer_class = ContentFinderConditionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            error_message = 'No conditions found with the given parameters'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        type_id = self.request.query_params.get('type')
        min_level = self.request.query_params.get('min')
        max_level = self.request.query_params.get('max')

        # For caching
        cache_key = f'content_finder_conditions_{type_id}_{min_level}_{max_level}'
        cached_response = cache.get(cache_key)

        if cached_response:
            return cached_response

        if not type_id or not min_level or not max_level:
            return ContentFinderCondition.objects.none()

        queryset = ContentFinderCondition.objects.filter(
            class_job_level_required__gte=min_level,
            class_job_level_required__lte=max_level,
            content_type_id=type_id
        )

        return queryset

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


class ContentFinderConditionBookmarkList(generics.ListAPIView):
    serializer_class = UserBookmarkRetrieveSerializer

    def list(self, request, pk, *args, **kwargs):
        if not pk:
            error_message = 'No condition id provided'
            return Response({'error': error_message}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset(pk)
        serializer = self.get_serializer(queryset, many=True)

        if not queryset.exists():
            error_message = 'No bookmarks found with the given parameters'
            return Response({'error': error_message}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self, pk):
        bookmarks = UserBookmark.objects.filter(content_finder_condition_id=pk)
        return bookmarks

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)


@api_view(['GET'])
def get_routes(request):
    routes = [
        'conditions/',
        'conditions/<int:pk>/bookmarks/'
    ]

    return Response(routes)
