## Create Serializer 작성
- create 메소드 상세 파악


## 전체 메커니즘 한번 더 환기
- 메인 화면에서 comment -> 유튜브 링크 입력하고 get 버튼 누르면 댓글 목록 뜨게끔
- get 버튼 api -> 프론트에서 api 조립할건지, 백엔드에서 할건지


Feat: YouTube 댓글 크롤링 API 완성 및 문서화 추가
- YouTube API Service 완전 구현
  - list_comment_threads: 댓글 가져오기 (페이징 지원)
  - get_video_details: 비디오 정보 조회 메서드 (향후 확장)
  - get_channel_details: 채널 정보 조회 메서드 (향후 확장)
  - 에러 처리 및 타임아웃 처리 구현
- Custom Exception 추가 (YouTubeAPIException)
  - YouTube API 관련 예외 처리 전용 클래스
- CommentSerializer 개선
  - YouTube URL/ID 검증 로직 추가 (validate_url)
  - video_id, max_results 필드 추가
  - 다양한 YouTube URL 형식 지원 (watch, embed, youtu.be)
- CommentViewSet 기능 확장
  - fetch_and_save custom action 추가
  - YouTube API Service 연동
- API 문서화 도구 추가 (DRF Spectacular)
  - Swagger UI 엔드포인트 추가 (/api/docs/)
  - OpenAPI Schema 엔드포인트 추가 (/api/schema/)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
