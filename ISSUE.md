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

---

## Issue 7: Todo stats 액션 — 다중 쿼리에서 단일 쿼리로 개선

**문제:**
- Todo 통계(전체/완료/미완료 개수)를 조회할 때 쿼리를 3번 개별적으로 실행

**변경 전 (쿼리 3회):**
```python
def stats(self, request):
    todos = self.get_queryset()
    total = todos.count()                          # 쿼리 1
    completed = todos.filter(completed=True).count()   # 쿼리 2
    pending = todos.filter(completed=False).count()    # 쿼리 3
    return Response({...})
```

**변경 후 (쿼리 1회):**
```python
def stats(self, request):
    todos = self.get_queryset()
    stats = todos.aggregate(
        total_count=Count('id'),
        completed_count=Count('id', filter=Q(completed=True)),
        pending_count=Count('id', filter=Q(completed=False)),
    )
    return Response(stats)
```

**장점:**
- DB 왕복 3회 → 1회로 감소하여 네트워크 오버헤드 및 응답 시간 개선
- `aggregate`는 단일 SQL에서 `COUNT`와 `CASE WHEN`으로 처리되어 DB가 테이블을 한 번만 스캔
- 3개의 값이 동일 시점의 스냅샷에서 계산되므로 데이터 정합성 보장 (다중 쿼리 시 사이에 데이터 변경 가능성 존재)
- 통계 항목이 추가되어도 쿼리 수가 늘어나지 않아 확장에 유리

---

## Issue 8: 쿼리 파라미터 필터링 — 별도 엔드포인트 vs get_queryset 오버라이드

**문제:**
- 목록 조회 시 조건별 필터링(video_id, completed, hidden 등)을 어떻게 처리할지 설계 필요
- 처음에는 필터 조건마다 별도 엔드포인트(커스텀 액션)를 만들어 사용했으나, `get_queryset`에서 쿼리 파라미터에 따라 동적으로 필터링하는 방식으로 변경

**변경 전 — 별도 엔드포인트 방식:**
```python
# 조건마다 커스텀 액션 생성
@action(detail=False, methods=['get'], url_path='completed')
def completed_list(self, request):
    queryset = Todo.objects.filter(completed=True)
    ...

@action(detail=False, methods=['get'], url_path='hidden')
def hidden_list(self, request):
    queryset = Todo.objects.filter(hidden=True)
    ...
```

**변경 후 — get_queryset 오버라이드 방식:**
```python
# todos/views.py
def get_queryset(self):
    queryset = Todo.objects.all()
    if not include_hidden:
        queryset = queryset.filter(hidden=False)
    if completed_param is not None:
        queryset = queryset.filter(completed=is_completed)
    return queryset

# comments/views.py
def get_queryset(self):
    queryset = Comment.objects.all()
    video_id = self.request.query_params.get("video_id")
    if video_id:
        queryset = queryset.filter(video_id=video_id)
    return queryset
```

### 방식 1: 별도 엔드포인트 (커스텀 액션)

| 장점 | 단점 |
|---|---|
| 각 엔드포인트의 역할이 명확하고 URL만으로 의도 파악 가능 | 필터 조건이 늘어날수록 엔드포인트가 비례하여 증가 |
| 엔드포인트별로 독립적인 권한/스로틀 설정 가능 | 조건 조합이 필요하면 (예: 완료 + 숨김) 엔드포인트가 폭발적으로 증가 |
| API 문서에서 각 기능이 개별 항목으로 노출 | 필터링 로직이 여러 메서드에 분산되어 중복 코드 발생 |

### 방식 2: get_queryset 오버라이드 (채택)

| 장점 | 단점 |
|---|---|
| 단일 엔드포인트에서 쿼리 파라미터 조합으로 유연한 필터링 가능 | URL만으로 어떤 필터가 지원되는지 파악 어려움 |
| 필터 조건 추가 시 get_queryset에 조건문만 추가하면 됨 | 파라미터 검증 로직이 복잡해질 수 있음 |
| DRF의 list/retrieve/stats 등 모든 액션에 필터가 자동 적용 | 엔드포인트별 세밀한 권한 분리가 어려움 |
| REST 컨벤션에 부합 (`GET /todos/?completed=true&hidden=true`) | |

**결론:**
- 단순 필터링 조건은 `get_queryset` 오버라이드로 처리하는 것이 REST 컨벤션에 맞고 유지보수에 유리
- `get_queryset`에서 필터링하면 `list`, `stats` 등 queryset을 사용하는 모든 액션에 일관되게 적용되는 이점이 있음
- 별도 엔드포인트는 필터링이 아닌 완전히 다른 비즈니스 로직(예: `fetch-and-save`, `toggle`)에 적합
