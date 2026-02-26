## Create Serializer 작성
- create 메소드 상세 파악


## 전체 메커니즘 한번 더 환기
- 메인 화면에서 comment -> 유튜브 링크 입력하고 get 버튼 누르면 댓글 목록 뜨게끔
- get 버튼 api -> 프론트에서 api 조립할건지, 백엔드에서 할건지

마지막 커밋 이후의 변경사항에 대한 작업 내용을 이전 커밋 메시지들을 참고하여 가능한 간단하게 COMMIT.md의 맨 마지막에 작성해주시고, 커밋은 하지마세요.

serializer video_id = serializers...
serializers/validate_url - pattern, _ in id 
serializer_isvalid

db 어떻게 되어있는지 확인
다른 기능 mp3
serializers check₩

Chore: uv 개발 패키지 분리
- black, ruff 개발 패키지로 분리 및 전체 프로젝트에 적용
- .gitignore에 데이터베이스, migrations 관련 설정 추가

Feat: Todo ViewSet 및 모델 개선 / Comments 리팩토링
- Todo 모델: content 필드 CharField(max_length=20)로 변경, description 필드 추가
- Todo Serializer: 액션별 Serializer 분리 (Create/List/Detail/Update/Delete)
- Todo ViewSet: 기본 CRUD 구조 작성, hidden 필터링 구현
- Comments ViewSet: url_path를 REST 컨벤션(fetch-and-save)으로 수정, max_results 500으로 변경, bulk 저장 시 BaseCommentSerializer 사용으로 변경
- ISSUE.md: Todo 제목 길이 제한 검증 로직 위치 설계 문서화 (Issue 6)

Feat: Todo ViewSet 커스텀 액션 추가 및 queryset 필터링 개선
- Todo ViewSet: toggle, hide, stats 커스텀 액션 추가
- get_queryset: completed 파라미터 필터링 추가
- stats: aggregate 단일 쿼리로 통계 조회 구현
- ISSUE.md: stats 다중 쿼리 → 단일 쿼리 개선 문서화 (Issue 7)

Feat: Comment 모델 snake_case 전환 및 stats 액션 추가
- Comment 모델: 필드명 camelCase → snake_case로 변경
- Comments ViewSet: get_queryset 오버라이드로 video_id 필터링 추가, stats/stats_timeline 액션 추가
- ISSUE.md: 쿼리 파라미터 필터링 설계 문서화 (Issue 8)
- pyproject.toml: konlpy 패키지 추가

Feat: videos 앱 추가 및 word-frequency 액션 활성화
- videos 앱 생성, INSTALLED_APPS 등록
- Video/Playlist 모델 정의 (ziip/models.py)
- Comments ViewSet: list 내 중복 video_id 필터링 제거, word_frequency 액션 주석 해제

Refactor: 앱 구조 도메인 네임스페이스 재구성 및 신규 서비스 스텁 추가
- comments, videos → youtube/comments, youtube/videos 로 이동
- todos → utils/todos 로 이동
- web/crawling 앱 신규 추가 (HackerNews 크롤링 서비스 스텁)
- core/services/translation_service.py: DeepL 번역 서비스 스텁 추가
- pyproject.toml: beautifulsoup4, deepl, httpx 의존성 추가
- Chore: 프로젝트명 youtility → ziip 변경, 문서 업데이트