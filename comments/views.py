from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.exceptions import YouTubeAPIException
from core.services import YoutubeAPIService
from .models import Comment
from .serializers import BaseCommentSerializer, CommentCreateSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 가져오기

    list: 저장된 댓글 목록 조회
    retrieve: 특정 댓글 상세 조회
    fetch_and_save: youtube에서 댓글 가져와서 저장 (custom action)
    """
    queryset = Comment.objects.all()
    serializer_class = BaseCommentSerializer

    def get_serializer_class(self):
        if self.action == 'fetch_and_save':
            return CommentCreateSerializer
        return BaseCommentSerializer

    @action(detail=False, methods=['post'], url_path='fetch_and_save')
    def fetch_and_save(self, request):
        input_serializer = BaseCommentSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        video_id = input_serializer.validated_data['video_id']

        youtube_service = YoutubeAPIService()

        try:
            api_response = youtube_service.list_comment_threads(video_id=video_id)
        except YouTubeAPIException as e:
            return Response(
                {'error': str(e)},
                status=e.status_code
            )

        comments_data = self._process

    def _process_youtube_response(
            self,
            api_response: dict,
            video_id: str,
    )-> list:

        comments_data = []

        for item in api_response.get('items', []):
            snippet = item['snippet']['topLevelComment']['snippet']

            comments_data = {
                'video_id': video_id,
                'comment_id': item['id'],
                'comment_text': snippet['text'],
                'comment_date': snippet['publishedAt'],
            }


