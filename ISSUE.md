# Issue Log

## Issue 1: 백엔드-프론트엔드 API 연결 불일치

**문제:**
- 프론트엔드: POST `/comments/` 호출
- 백엔드: POST `/comments/fetch_and_save/` 필요
- 요청 데이터 형식 불일치 (`video_url` vs `video_id`)

**원인:**
- API 엔드포인트 및 요청 형식이 서로 다름
- 백엔드 serializers.py에 오타 (validate_url → validate_video_id)
- 백엔드 views.py에 오타 (appends, 딕셔너리 구문)

**해결:**
- 프론트엔드 api.js 수정: `crawlComments`, `getComments` 분리
- 백엔드 serializers.py: URLInputSerializer → Serializer로 변경, validate_video_id로 수정
- 백엔드 views.py: 오타 수정

---

## Issue 2: CORS 설정 누락

**문제:**
- 프론트엔드(localhost:5173)에서 백엔드(localhost:8000) 요청 시 CORS 에러

**원인:**
- django-cors-headers 설치는 되어 있으나 settings.py 미설정

**해결:**
```python
# settings.py
INSTALLED_APPS = [..., 'corsheaders']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ...]
CORS_ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]
```

---

## Issue 3: YouTube API 페이징 미처리 (20개만 저장)

**문제:**
- 80개 이상 댓글이 있어도 20개만 DB 저장

**원인:**
- YouTube API를 한 번만 호출 (첫 페이지만 가져옴)
- nextPageToken을 사용한 페이징 처리 없음

**해결:**
```python
# views.py fetch_and_save
while True:
    api_response = youtube_service.list_comment_threads(
        video_id=video_id,
        max_results=max_results,
        page_token=page_token
    )
    all_comments_data.extend(comments_data)
    page_token = api_response.get('nextPageToken')
    if not page_token:
        break
```

---

## Issue 4: 프론트엔드 댓글 조회 페이지 누락

**문제:**
- 크롤 후 댓글 조회 페이지가 없음

**원인:**
- 댓글 저장 후 list 반환 페이지 미구현 (`comments/{videoId}` 페이지 전환)

**해결:**
- `CommentDetail.jsx` 페이지 추가
- 라우팅 추가: `/comments/:videoId`
- `CommentUtility.jsx` 수정: 크롤 성공 후 페이지 전환 (`navigate`)

---

## Issue 5: DRF 페이징 설정 누락 (조회 실패)

**문제:**
- DB에 데이터는 저장되지만 프론트엔드에서 조회 시 "댓글이 없습니다" 표시

**원인:**
- DRF DEFAULT_PAGINATION_CLASS 미설정
- 페이징 없이는 응답 형식이 달라짐 (배열 vs {count, results})

**해결:**
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```
