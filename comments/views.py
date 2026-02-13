from typing import Counter

from django.db import transaction
from django.db.models import Count, Avg, Max
from django.db.models.functions import TruncDate
from konlpy.tag import Okt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from core.exceptions import YouTubeAPIException
from core.services import YoutubeAPIService
from .models import Comment
from .serializers import *


class CommentViewSet(viewsets.ModelViewSet):
    """
    댓글 가져오기

    list: 저장된 댓글 목록 조회
    retrieve: 특정 댓글 상세 조회
    fetch_and_save: youtube에서 댓글 가져와서 저장 (custom action)
    """

    serializer_class = BaseCommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        video_id = self.request.query_params.get("video_id")

        if video_id:
            queryset = queryset.filter(video_id=video_id)

        return queryset

    # 액션별로 다른 Serializer 할당, 현재는 의미없음 (fetch and save 에서는 별도의 bulk 메서드 사용)
    def get_serializer_class(self):
        if self.action == "fetch-and-save":
            return CommentCreateSerializer
        return BaseCommentSerializer

    @action(detail=False, methods=["post"], url_path="fetch-and-save")  # rest 컨벤션
    def fetch_and_save(self, request):
        input_serializer = URLInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        video_id = input_serializer.validated_data["video_id"]
        max_results = input_serializer.validated_data.get("max_results", 500)

        youtube_service = YoutubeAPIService()
        all_comments_data = []
        page_token = None

        try:
            # 모든 댓글을 가져올 때까지 페이징 처리
            while True:
                api_response = youtube_service.list_comment_threads(
                    video_id=video_id, max_results=max_results, page_token=page_token
                )

                comments_data = self._process_youtube_response(api_response, video_id)
                all_comments_data.extend(comments_data)

                # 다음 페이지가 있는지 확인
                page_token = api_response.get("nextPageToken")
                if not page_token:
                    break

        except YouTubeAPIException as e:
            return Response({"error": str(e)}, status=e.status_code)

        if not all_comments_data:
            return Response({"message": "댓글이 없습니다."}, status=status.HTTP_200_OK)

        saved_comments = self._bulk_save_comments(all_comments_data)

        return Response(
            {
                "message": f"{len(saved_comments)}개의 댓글을 저장했습니다.",
                "video_id": video_id,
                "total_comments": len(all_comments_data),
                "saved_comments": len(saved_comments),
            },
            status=status.HTTP_201_CREATED,
        )

    def _process_youtube_response(
            self,
            api_response: dict,
            video_id: str,
    ) -> list:

        comments_data = []

        for item in api_response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]

            comment_data = {
                "video_id": video_id,
                "comment_id": item["snippet"]["topLevelComment"]["id"],
                "author_display_name": snippet["authorDisplayName"],
                "author_channel_url": snippet["authorChannelUrl"],
                "text_display": snippet["textDisplay"],
                "text_original": snippet["textOriginal"],
                "like_count": snippet["likeCount"],
                "published_at": snippet["publishedAt"],
                "updated_at": snippet["updatedAt"],
            }
            comments_data.append(comment_data)

        return comments_data

    @transaction.atomic
    def _bulk_save_comments(
            self,
            comments_data: list,
    ) -> list:
        saved_comments = []

        for comment in comments_data:
            if Comment.objects.filter(comment_id=comment["comment_id"]).exists():
                continue

            serializer = BaseCommentSerializer(data=comment)
            if serializer.is_valid():
                saved_comment = serializer.save()
                saved_comments.append(saved_comment)

        return saved_comments

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        comments = self.get_queryset()

        basic_stats = comments.aggregate(
            total_comments=Count("comment_id"),
            avg_likes=Avg("like_count"),
            max_likes=Max("like_count"),
        )

        top_comments = comments.order_by("-like_count")[:10].value(
            'comment_id', 'text_display', "like_count", "author_display_name"
        )
        return Response(
            {
                "total_comments": basic_stats["total_comments"],
                "avg_likes": basic_stats["avg_likes"],
                "max_likes": basic_stats["max_likes"],
                "top_comments": top_comments
            }
        )

    @action(detail=False, methods=["get"], url_path="stats/timeline")
    def stats_timeline(self, request):
        comments = self.get_queryset()

        # QQQ
        timeline = comments.annotate(
            date=TruncDate("published_at")
        ).values("date").annotate(
            count=Count("id")
        ).order_by("date")

        return Response(list(timeline))

    @action(detail=False, methods=["get"], url_path="word-frequency")
    def word_frequency(self, request):
        comments = self.get_queryset()

        all_text = ' '.join(comments.values_list("text_display", flat=True))

        # 형태소 분석 (추후 언어별 모델 추가 예정)
        okt = Okt()
        nouns = okt.nouns(all_text)

        # 불용어 제거
        stopwords = ['이', '그', '저', '것', '수', '등', '때']
        filtered_nouns = [word for word in nouns if word not in stopwords and len(word) > 1]

        word_counts = Counter(filtered_nouns)
        top_words = word_counts.most_common(50)

        return Response(
            {'total_words': len(filtered_nouns),
             'unique_words': len(word_counts),
             'top_words': [
                 {'word': word, 'count': count}
                 for word, count in top_words
             ]}
        )