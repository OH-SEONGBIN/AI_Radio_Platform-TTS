# 🎙️ AI TTS 기반 라디오 플랫폼

AI 음성 합성(TTS)와 웹 개발 전과정을 경험하는 토이 프로젝트  
(본인만의 라디오를 만들고 방송하는 실습용 플랫폼)

---

## 📌 프로젝트 한눈에 보기

- **TTS 기반 온라인 라디오**: AI 음성합성으로 방송 생성/시청/공유  
- **실습 포인트**  
  - 프론트-백엔드 전체 설계/구현/연동
  - Jenkins, Docker 기반 CI/CD 파이프라인 경험
  - 실무형 API 인증, 보안(.gitignore 등) 적용
- **직접 경험한 내용만 포함!**  
  → 포트폴리오, 실무 코딩테스트/면접에 바로 활용 가능

---

## 🗂️ 폴더 구조

```plaintext
├── backend/         # Python FastAPI(Flask) TTS/REST API
├── frontend/        # React/Vue/HTML SPA UI
├── requirements.txt # 백엔드 의존성
├── .gitignore
├── README.md

```

🚦 주요 기능 요약
회원가입/로그인/인증

AI 음성합성(TTS) 라디오 방송 생성

카테고리별 방송 시청

방송 녹음/공유 기능

CI/CD 자동화(Jenkins, Docker) 실습

⚙️ 기술 스택
분야	기술
백엔드	Python, FastAPI(Flask), REST API, Google TTS
프론트엔드	React, HTML/CSS/JS, Axios
CI/CD	Jenkins, Docker, GitHub Actions
기타	JWT 인증, .env, .gitignore

🚀 실행 방법(실전 예시)
1. 백엔드 서버 실행
```bash

cd backend
pip install -r requirements.txt
python app.py
```
2. 프론트엔드 서버 실행
```bash

cd ../frontend
npm install
npm start
3. Jenkins 파이프라인 연동
Jenkinsfile 참고
```
실습용 Jenkins, Docker 이미지에서 pytest 자동 테스트/배포

📝 실습/포트폴리오 주요 학습 내용
- TTS+웹서비스 아키텍처 경험

- CI/CD 자동화 경험

- 보안 민감정보 커밋방지(.gitignore) 실습

- 실무 프로젝트 구조 직접 설계/구현/배포

📸 대표 UI (스크린샷/링크)
(Notion에선 이미지 첨부, GitHub에선 링크/캡처 첨부 권장)

🛡️ 주의사항 및 보안 정책
- Google Cloud 서비스키 등 민감정보는 .gitignore로 반드시 보호

- 개인 실습/포트폴리오용으로만 활용 (외부 서비스 배포 전 별도 보안 점검 필요)

🙋‍♂️ 개발/실습: 오성빈
- 깃허브: OH-SEONGBIN

- 추가 질문/참여/리뷰는 이슈로 남겨주세요!
