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

---

## Issue 6: Todo 제목 길이 제한 — 검증 로직 위치 설계

**문제:**
- 할일(Todo) 제목의 길이를 제한해야 하는데, 검증 로직을 어디에 배치할지 결정이 필요

**검토한 3가지 옵션:**

### 옵션 1: Model의 `max_length`로 제한 (채택)

```python
# models.py
title = models.CharField(max_length=100)
```

| 장점 | 단점 |
|---|---|
| DB 레벨에서 제약이 걸려 어떤 경로로든 데이터 무결성 보장 | 제한 길이 변경 시 마이그레이션 필요 |
| Serializer, Form, Admin 등에서 자동으로 max_length 반영 | 에러 메시지 커스터마이징이 제한적 |
| 단일 진실 원천(Single Source of Truth)으로 관리 용이 | |

### 옵션 2: Serializer의 field 옵션에서 제한

```python
# serializers.py
title = serializers.CharField(max_length=100)
```

| 장점 | 단점 |
|---|---|
| 마이그레이션 없이 제한 길이 변경 가능 | DB 레벨 보호 없음 (Shell, Admin 등에서 긴 값 입력 가능) |
| API 입력 검증에 특화 | Model과 Serializer의 제한이 불일치할 위험 |
| DRF 표준 에러 응답 자동 생성 | |

### 옵션 3: Serializer의 `validate_<field>` 메서드로 제한

```python
# serializers.py
def validate_title(self, value):
    if len(value) > 100:
        raise serializers.ValidationError("제목은 100자 이내여야 합니다.")
    return value
```

| 장점 | 단점 |
|---|---|
| 에러 메시지를 자유롭게 커스터마이징 가능 | 단순 길이 제한에 비해 코드가 과함 (오버엔지니어링) |
| 조건부 검증 등 복잡한 로직 적용 가능 | DB 레벨 보호 없음 |
| | 다른 Serializer에서 동일 검증을 반복해야 할 수 있음 |

**결론:**
- 제목 길이 제한은 단순한 제약 조건이므로, **Model의 `max_length`로 직접 제한하는 옵션 1을 채택**
- Model에서 정의하면 DB 레벨 무결성이 보장되고, Serializer가 Model 필드 정보를 자동으로 상속받아 중복 정의 없이 일관된 검증이 가능
