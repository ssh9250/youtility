# ziip 프로젝트 요약 문서

## 1. 프로젝트 개요

**ziip**은 YouTube 동영상의 댓글을 크롤링하고 분석할 수 있는 웹 애플리케이션입니다.

### 주요 목적
- YouTube 동영상의 전체 댓글을 수집하여 데이터베이스에 저장
- 수집된 댓글을 조회하고 페이징 처리
- 향후 댓글 분석 및 유틸리티 기능 확장 예정

---

## 2. 기술 스택

### 백엔드
- **Python**: 3.14
- **Django**: 6.0
- **Django REST Framework**: 3.16.1
- **데이터베이스**: SQLite (개발 환경)
- **주요 패키지**:
  - `django-cors-headers`: 4.9.0 (CORS 처리)
  - `drf-spectacular`: 0.29.0 (API 문서화)
  - `python-decouple`: 3.8 (환경 변수 관리)
  - `requests`: 2.32.5 (YouTube API 통신)

### 프론트엔드
- **React**: 19.2.0
- **React Router DOM**: 7.11.0
- **Axios**: 1.13.2 (API 통신)
- **Vite**: 7.2.4 (빌드 도구)
- **개발 서버**: localhost:5173

### 개발 도구
- **Black**: 코드 포맷터
- **Ruff**: Linter
- **Pytest**: 테스트 프레임워크
- **uv**: 패키지 매니저

### 외부 API
- **YouTube Data API v3**: 댓글 수집

---

## 3. 프로젝트 구조

```
ziip/
├── ziip/                      # Django 프로젝트 설정
│   ├── settings.py            # 프로젝트 설정 (CORS, DRF, DB 등)
│   ├── urls.py                # 메인 URL 라우팅
│   ├── wsgi.py                # WSGI 설정
│   └── asgi.py                # ASGI 설정
│
├── core/                      # 핵심 서비스 레이어
│   ├── exceptions.py          # 커스텀 예외 (YouTubeAPIException)
│   └── services/
│       └── youtube_api_service.py  # YouTube API 통신 서비스
│
├── comments/                  # 댓글 앱
│   ├── models.py              # Comment 모델
│   ├── views.py               # CommentViewSet (API 뷰)
│   ├── serializers.py         # Serializers (검증, 직렬화)
│   ├── urls.py                # URL 라우팅
│   ├── admin.py               # Admin 설정
│   └── migrations/            # DB 마이그레이션
│
├── Frontend/                  # React 프론트엔드
│   ├── src/
│   │   ├── App.jsx            # 메인 앱 (라우팅)
│   │   ├── main.jsx           # 진입점
│   │   ├── services/
│   │   │   └── api.js         # API 통신 (axios)
│   │   ├── pages/
│   │   │   ├── Home.jsx       # 홈 페이지
│   │   │   ├── CommentUtility.jsx    # 댓글 크롤링 페이지
│   │   │   ├── CommentDetail.jsx     # 댓글 조회 페이지
│   │   │   └── EmptyPage.jsx  # 플레이스홀더 페이지
│   │   └── components/
│   │       ├── Navigation.jsx  # 네비게이션
│   │       ├── CommentList.jsx # 댓글 리스트
│   │       └── Pagination.jsx  # 페이징
│   └── package.json           # 프론트엔드 의존성
│
├── manage.py                  # Django 관리 명령
├── pyproject.toml             # Python 패키지 설정 (uv)
├── .env                       # 환경 변수 (gitignore)
├── .env.example               # 환경 변수 예시
├── README.md                  # 프로젝트 문서
└── ISSUE.md                   # 개발 중 발생한 이슈 로그
```

---

## 4. 주요 기능

### 4.1 YouTube 댓글 크롤링
- YouTube 동영상 URL 또는 Video ID 입력
- YouTube Data API v3를 통한 전체 댓글 수집
- **페이징 처리**: `nextPageToken`을 사용하여 모든 댓글 수집
- 중복 방지: `comment_id`로 기존 댓글 필터링
- 트랜잭션 처리: `@transaction.atomic`으로 안전한 저장

### 4.2 댓글 조회
- video_id별 댓글 필터링
- DRF Pagination (20개 단위)
- 좋아요 수(`likeCount`) 기준 정렬 (내림차순)

### 4.3 API 문서화
- **Swagger UI**: `/api/docs/`
- **OpenAPI Schema**: `/api/schema/`

---

## 5. API 엔드포인트

### 백엔드 API (localhost:8000)

| Method | Endpoint | 설명 | 요청 파라미터 |
|--------|----------|------|--------------|
| POST | `/api/comments/fetch_and_save/` | YouTube에서 댓글 크롤링 및 DB 저장 | `video_id`, `max_results` (optional) |
| GET | `/api/comments/` | 저장된 댓글 목록 조회 | `video_id`, `page` (query params) |
| GET | `/api/comments/{id}/` | 특정 댓글 상세 조회 | - |
| GET | `/api/docs/` | Swagger UI | - |
| GET | `/api/schema/` | OpenAPI Schema | - |

#### 5.1 POST `/api/comments/fetch_and_save/`

**요청 예시:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "max_results": 100  // optional, default: 100
}
```

**응답 예시:**
```json
{
  "message": "150개의 댓글을 저장했습니다.",
  "video_id": "dQw4w9WgXcQ",
  "total_comments": 150,
  "saved_comments": 150
}
```

**지원되는 video_id 형식:**
- Video ID: `dQw4w9WgXcQ`
- YouTube URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- 짧은 URL: `https://youtu.be/dQw4w9WgXcQ`
- Embed URL: `https://www.youtube.com/embed/dQw4w9WgXcQ`

#### 5.2 GET `/api/comments/`

**요청 예시:**
```
GET /api/comments/?video_id=dQw4w9WgXcQ&page=1
```

**응답 예시:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/comments/?page=2&video_id=dQw4w9WgXcQ",
  "previous": null,
  "results": [
    {
      "id": 1,
      "comment_id": "UgwL...",
      "video_id": "dQw4w9WgXcQ",
      "authorDisplayName": "John Doe",
      "authorChannelUrl": "http://www.youtube.com/channel/...",
      "textDisplay": "Great video!",
      "textOriginal": "Great video!",
      "likeCount": 42,
      "publishedAt": "2024-01-01T12:00:00Z",
      "updatedAt": "2024-01-01T12:00:00Z"
    }
  ]
}
```

---

## 6. 데이터 모델

### Comment 모델 (comments/models.py)

**사용 기술**: Django ORM (`django.db.models.Model`)

```python
class Comment(models.Model):
    comment_id = models.CharField(max_length=255, verbose_name="댓글 id")
    video_id = models.CharField(max_length=255, verbose_name="동영상 id")
    authorDisplayName = models.CharField(max_length=100, verbose_name="작성자")
    authorChannelUrl = models.TextField(blank=True, verbose_name="작성자 채널 주소")
    textDisplay = models.TextField(blank=True, verbose_name="내용")
    textOriginal = models.TextField(blank=True, verbose_name="내용 원본")
    likeCount = models.IntegerField(verbose_name="좋아요 수")
    publishedAt = models.DateTimeField("작성일")
    updatedAt = models.DateTimeField("수정일")

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        db_table = "comments"
        ordering = ["-likeCount"]
```

**주요 특징**:
- Django의 `models.Model` 상속
- `Meta` 클래스로 테이블명, 정렬 기준 설정
- **테이블명**: `comments`
- **정렬 기준**: `-likeCount` (좋아요 수 내림차순)
- 한글 verbose_name으로 Admin 페이지 가독성 향상

---

## 7. Views와 Serializers

### 7.1 CommentViewSet (comments/views.py)

**사용 기술**: DRF `viewsets.ModelViewSet`

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.db import transaction

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = BaseCommentSerializer
```

**주요 특징**:
- **`viewsets.ModelViewSet`**: CRUD 자동 생성 (list, retrieve, create, update, destroy)
- **Custom Action**: `@action` 데코레이터로 `fetch_and_save` 커스텀 엔드포인트 추가
- **동적 Serializer**: `get_serializer_class()`로 액션별 다른 Serializer 사용
- **트랜잭션 처리**: `@transaction.atomic`으로 일괄 저장 시 데이터 무결성 보장
- **페이징**: DRF의 자동 페이징 적용 (settings.py 설정)

**주요 메서드**:

1. **`fetch_and_save`** (custom action)
   - HTTP Method: POST
   - URL: `/api/comments/fetch_and_save/`
   - 기능: YouTube API 호출 → 댓글 수집 → DB 저장
   - 특징: while 루프로 `nextPageToken` 처리하여 전체 댓글 수집

2. **`list`** (override)
   - HTTP Method: GET
   - URL: `/api/comments/`
   - 기능: 댓글 목록 조회, video_id 필터링
   - 특징: query parameter로 `video_id` 받아 필터링

3. **`_process_youtube_response`** (private helper)
   - YouTube API 응답을 Comment 모델 형식으로 변환

4. **`_bulk_save_comments`** (private helper)
   - `@transaction.atomic`으로 댓글 일괄 저장
   - 중복 체크 (`comment_id` 기준)

### 7.2 Serializers (comments/serializers.py)

**사용 기술**: DRF `serializers.ModelSerializer`, `serializers.Serializer`

#### URLInputSerializer
```python
from rest_framework import serializers

class URLInputSerializer(serializers.Serializer):
    video_id = serializers.CharField(max_length=255)
    max_results = serializers.IntegerField(default=100, min_value=1, max_value=200)

    def validate_video_id(self, value):
        # YouTube URL → Video ID 추출 로직
```

**특징**:
- **`serializers.Serializer`**: 모델과 무관한 입력 검증용
- **커스텀 검증**: `validate_video_id`로 YouTube URL 파싱
- 다양한 YouTube URL 형식 지원 (watch, youtu.be, embed)
- 정규표현식으로 11자리 Video ID 추출

#### BaseCommentSerializer
```python
class BaseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
```

**특징**:
- **`serializers.ModelSerializer`**: Comment 모델 기반 자동 직렬화
- 모든 필드 노출 (`fields = "__all__"`)
- 조회 API에서 사용

#### CommentCreateSerializer
```python
class CommentCreateSerializer(BaseCommentSerializer):
    def validate_comment_id(self, value):
        if Comment.objects.filter(comment_id=value).exists():
            raise serializers.ValidationError("이미 저장된 댓글입니다.")
        return value
```

**특징**:
- **BaseCommentSerializer 상속**: Comment 모델 기반
- **중복 검증**: `validate_comment_id`로 기존 댓글 체크
- 저장 API에서 사용

---

## 8. 핵심 서비스 레이어

### YoutubeAPIService (core/services/youtube_api_service.py)

YouTube Data API v3와 통신하는 서비스 클래스입니다.

#### 주요 메서드:

1. **`list_comment_threads(video_id, part='snippet', max_results=200, page_token=None)`**
   - 동영상의 댓글 스레드 목록 조회
   - 페이징 지원 (`page_token` 파라미터)

2. **`get_video_details(video_id, part='snippet,contentDetails,statistics')`**
   - 비디오 상세 정보 조회 (향후 확장 예정)

3. **`get_channel_details(channel_id, part='snippet,contentDetails,statistics')`**
   - 채널 상세 정보 조회 (향후 확장 예정)

#### 에러 처리:
- `YouTubeAPIException`: 커스텀 예외 클래스
- Timeout, HTTPError, RequestException 처리
- API 에러 응답 파싱

---

## 9. 개발 환경 설정

### 9.1 환경 변수 (.env)

```bash
# Django 설정
SECRET_KEY=your-secret-key
DEBUG=True

# 데이터베이스 (SQLite)
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

# YouTube Data API v3
YOUTUBE_DATA_API_V3_SECRET=your-youtube-api-key
YOUTUBE_DATA_API_V3_URL=https://www.googleapis.com/youtube/v3/comments
```

### 9.2 백엔드 실행

```bash
# 1. 의존성 설치
uv sync

# 2. 마이그레이션
python manage.py migrate

# 3. 개발 서버 실행
python manage.py runserver
```

### 9.3 프론트엔드 실행

```bash
cd Frontend

# 1. 의존성 설치
npm install

# 2. 개발 서버 실행
npm run dev
```

---

## 10. 중요 설정 (settings.py)

### 10.1 CORS 설정

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 최상단 배치
    # ...
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
```

### 10.2 DRF 설정

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### 10.3 Spectacular (API 문서화) 설정

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'config',
    'DESCRIPTION': 'API documentation for config',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
}
```

---

## 11. 빠른 참조

### API Base URL
- 백엔드: `http://localhost:8000/api`
- 프론트엔드: `http://localhost:5173`

### 주요 명령어
```bash
# 백엔드
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser  # Admin 계정 생성

# 프론트엔드
npm run dev
npm run build

# 코드 포맷팅/린팅
black .
ruff check .
```

### Admin 페이지
- URL: `http://localhost:8000/admin/`
- Comment 모델 관리 가능

---

## 12. 참고 자료

- [Django 6.0 공식 문서](https://docs.djangoproject.com/en/6.0/)
- [Django REST Framework 문서](https://www.django-rest-framework.org/)
- [YouTube Data API v3 문서](https://developers.google.com/youtube/v3/docs)
- [React Router DOM 문서](https://reactrouter.com/)

---

**마지막 업데이트**: 2026-01-07
**프로젝트 버전**: 0.1.0
