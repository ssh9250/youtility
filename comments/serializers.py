from rest_framework import serializers
from .models import Comment


class BaseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    video_id = serializers.CharField(
        max_length=255,
        help_text="Youtube Video URL 또는 Video ID",
    )
    max_results = serializers.IntegerField(
        default=100,
        min_value=1,
        max_value=200,
        help_text="가져올 댓글 개수 (최대 200)"
    )

    def validate_url(self, value):
        import re

        if len(value) == 11 and value.isalnum():
            return value

        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
        ]

        for pattern in patterns:
            match = re.search(pattern, value)
            if match:
                return match.group(1)

        raise serializers.ValidationError(
            "올바른 YouTube URL 또는 비디오 ID를 입력해주세요."
        )

class CommentCreateSerializer(BaseCommentSerializer):
    def validate_comment_id(self, value):
        if Comment.objects.filter(id=value).exists():
            raise serializers.ValidationError('이미 저장된 댓글입니다.')
        return value