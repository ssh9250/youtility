import requests
from django.conf import settings
from datetime import datetime, timezone
from typing import Any


class NewsService:
    """News API를 통한 종목 관련 뉴스 수집."""

    BASE_URL = "https://newsapi.org/v2/everything"

    def __init__(self):
        # self.api_key = settings.NEWS_API_KEY
        pass

    def fetch_for_ticker(self, ticker: str, days: int = 1) -> list[dict[str, Any]]:
        """
        티커 관련 최신 뉴스 조회.
        반환: [{"title": ..., "url": ..., "source": ..., "published_at": ...}, ...]
        """
        # params = {
        #     "q": ticker,
        #     "sortBy": "publishedAt",
        #     "pageSize": 10,
        #     "apiKey": self.api_key,
        #     "from": (datetime.now(timezone.utc) - timedelta(days=days)).isoformat(),
        # }
        # response = requests.get(self.BASE_URL, params=params, timeout=10)
        # response.raise_for_status()
        # articles = response.json().get("articles", [])
        # return self._normalize(articles)
        return []

    @staticmethod
    def _normalize(articles: list[dict]) -> list[dict[str, Any]]:
        """API 응답 → 내부 형식 변환."""
        result = []
        for a in articles:
            result.append({
                "title": a.get("title", ""),
                "summary": a.get("description", ""),
                "url": a.get("url", ""),
                "source": a.get("source", {}).get("name", ""),
                "published_at": a.get("publishedAt"),
            })
        return result