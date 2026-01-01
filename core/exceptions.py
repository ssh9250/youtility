# core/exceptions.py
from rest_framework.exceptions import APIException


class YouTubeAPIException(APIException):
    """YouTube API 관련 예외"""

    status_code = 503
    default_detail = "YouTube API 서비스를 사용할 수 없습니다."
    default_code = "youtube_api_unavailable"

    def __init__(self, detail=None, status_code=None):
        super().__init__(detail)
        if status_code:
            self.status_code = status_code
