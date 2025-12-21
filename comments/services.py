from django.conf import settings
from typing import Dict, Any

class OpenAPIService:
    """ 외부 API 호출을 담당하는 서비스 레이어 """

    def __init__(self):
        self.api_key = settings.YOUTUBE_DATA_API_V3_SECRET
        self.base_url = settings.YOUTUBE_DATA_API_V3_ENDPOINT

    def fetch_comments(self, address: str) -> Dict[str, Any]:
        params = {
            'api_key': self.api_key,
            'address': address,
        }