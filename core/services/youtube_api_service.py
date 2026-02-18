import requests
from django.conf import settings
from typing import Dict, Any, Optional

from core.exceptions import YouTubeAPIException


def _parse_error_response(response) -> str:
    """YouTube API 에러 응답 파싱"""
    try:
        error_data = response.json()
        if "error" in error_data:
            error_info = error_data["error"]
            message = error_info.get("message", "Unknown error")
            code = error_info.get("code", response.status_code)
            return f"[{code}] {message}"
    except:
        pass
    return f"Status {response.status_code}"


class YoutubeAPIService:
    BASE_URL = "https://youtube.googleapis.com/youtube/v3"

    def __init__(self):
        self.api_key = settings.YOUTUBE_DATA_API_V3_SECRET
        self.timeout = 10

    def _make_request(
        self,
        endpoint: str,
        params: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:

        default_headers = {
            "Accept": "application/json",
        }

        if headers:
            default_headers.update(headers)

        try:
            response = requests.get(endpoint, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise YouTubeAPIException("YouTube API 요청 시간 초과")
        except requests.HTTPError as e:
            error_detail = _parse_error_response(e.response)
            raise YouTubeAPIException(
                f"YouTube API 요청 실패: {error_detail}",
                status_code=e.response.status_code,
            )
        except requests.RequestException as e:
            raise YouTubeAPIException(f"네트워크 오류: {str(e)}")
        except ValueError:
            raise YouTubeAPIException("YouTube API 응답 파싱 실패")

    def list_comment_threads(
        self,
        video_id: str,
        part: str = "snippet",
        max_results: int = 200,
        page_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        endpoint = f"{self.BASE_URL}/commentThreads"
        params = {
            "part": part,
            "videoId": video_id,
            "key": self.api_key,
        }

        if page_token:
            params["pageToken"] = page_token

        return self._make_request(endpoint, params)

    # ========== Videos 관련 메서드 (향후 확장) ==========

    # todo: video 앱으로 이전
    def get_video_details(
        self, video_id: str, part: str = "snippet,contentDetails,statistics"
    ) -> Dict[str, Any]:
        """비디오 상세 정보 조회"""
        endpoint = f"{self.BASE_URL}/videos"
        params = {
            "part": part,
            "id": video_id,
            "key": self.api_key,
        }
        return self._make_request(endpoint, params)

    # ========== Channels 관련 메서드 (향후 확장) ==========

    def get_channel_details(
        self, channel_id: str, part: str = "snippet,contentDetails,statistics"
    ) -> Dict[str, Any]:
        """채널 상세 정보 조회"""
        endpoint = f"{self.BASE_URL}/channels"
        params = {
            "part": part,
            "id": channel_id,
            "key": self.api_key,
        }
        return self._make_request(endpoint, params)
