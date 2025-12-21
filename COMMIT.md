Feat: 환경 변수 관리 및 YouTube API 연동 준비
- python-decouple 추가하여 환경 변수 관리 구현
- .env 및 .env.example 파일 생성
- YouTube Data API v3 설정 추가
- OpenAPIService 클래스 구현 (외부 API 호출 서비스 레이어)
- .gitignore에 환경 변수 파일 제외 규칙 추가
- settings.py 리팩토링 (불필요한 주석 제거)

## Create Serializer 작성
- create 메소드 상세 파악


## 전체 메커니즘 한번 더 환기
- 메인 화면에서 comment -> 유튜브 링크 입력하고 get 버튼 누르면 댓글 목록 뜨게끔
- get 버튼 api -> 프론트에서 api 조립할건지, 백엔드에서 할건지

