from rest_framework import serializers

from youtube.videos.models import Video, DownloadTask


class VideoSerializer(serializers.ModelSerializer):
    # 비디오 정보 serializer
    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ('created_at')

class DownloadTaskSerializer(serializers.ModelSerializer):
    # 다운로드 작업 조회용 serializer

    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = DownloadTask
        fields = '__all__'
        read_only_fields = ('task_id', 'created_at')

class DownloadTaskCreateSerializer(serializers.ModelSerializer):
    # 다운로드 작업 생성용 serializer

    playlist_url = serializers.URLField(
        help_text="Youtube 재생목록 URL"
    )

    def validate_playlist_url(self , value):
        # 재생목록 검증
        import re

        patterns = [
            r'youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)',
            r'youtube\.com/watch\?.*list=([a-zA-Z0-9_-]+)',
        ]

        for pattern in patterns:
            match = re.match(pattern, value)
            if match:
                return value

        raise serializers.ValidationError(
            "올바른 재생목록 주소를 입력해주세요."
        )

class DownloadTaskStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = DownloadTask
        fields = '__all__'