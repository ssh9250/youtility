## Create Serializer 작성
- create 메소드 상세 파악


## 전체 메커니즘 한번 더 환기
- 메인 화면에서 comment -> 유튜브 링크 입력하고 get 버튼 누르면 댓글 목록 뜨게끔
- get 버튼 api -> 프론트에서 api 조립할건지, 백엔드에서 할건지


serializer video_id = serializers...
serializers/validate_url - pattern, _ in id 
serializer_isvalid

db 어떻게 되어있는지 확인
다른 기능 mp3
serializers check₩

Chore: uv 개발 패키지 분리
- black, ruff 개발 패키지로 분리 및 전체 프로젝트에 적용
- .gitignore에 데이터베이스, migrations 관련 설정 추가