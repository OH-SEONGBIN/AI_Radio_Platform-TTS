# 🎙️ AI TTS 기반 라디오 플랫폼

> **AI 음성 합성(TTS)을 활용해 누구나 손쉽게 온라인 라디오를 만들고,  
> 자신만의 이야기를 공유할 수 있는 프로젝트입니다.**

---

## 📋 프로젝트 소개

이 저장소는 AI 음성 합성(TTS)·백엔드·프론트엔드 통합 개발 실습의 결과물로,
- **TTS 엔진 기반 AI 라디오 서비스** 웹 플랫폼
- 음성 녹음, 청취, 회원가입 등 실사용 서비스 플로우 구현
- 클린코드 & CI/CD, 보안 best practice 적용

---

## 🏗️ 폴더 구조

├── backend/           # Python(FastAPI/Flask 등) 기반 백엔드
├── frontend/          # React/Vue/HTML 기반 프론트엔드
├── requirements.txt   # 백엔드 패키지 리스트
├── .gitignore
├── README.md
🚀 주요 기능
회원 가입 / 로그인 / 인증 / 게시글 작성 / 게시글 검색

라디오 방송 생성 & TTS 음성 합성

다양한 카테고리별 방송 시청

자체 Player UI/UX

🛠️ 기술 스택
구분	주요 기술
백엔드	Python, FastAPI/Flask, TTS API, RESTful API
프론트엔드	React, HTML/CSS/JS, Axios
배포/운영	GitHub Actions, Jenkins (실습), Docker
기타	Google Cloud TTS, JWT 인증, CI/CD

📝 빠른 시작

# 1. 백엔드 실행
cd backend
pip install -r requirements.txt
python app.py

# 2. 프론트엔드 실행
cd ../frontend
npm install
npm start

# 3. (실습용) Jenkins 파이프라인 연동/테스트
# Jenkinsfile 참고
📸 시연/스크린샷

<img width="1043" height="538" alt="_" src="https://github.com/user-attachments/assets/e26ac7e7-c0b6-4a46-b180-82bd88e7771d" />
<img width="1621" height="747" alt="5" src="https://github.com/user-attachments/assets/d990ad57-fa1c-41e8-a7b7-08cd74b89e8a" />

💡 실습 & 학습 포인트

TTS 기반 음성 라디오 플랫폼 아키텍처 설계 및 구축

백엔드-프론트엔드 실전 연동

실무형 CI/CD(Jenkins) 적용 경험

API 키/비밀키 등 민감 정보 안전 관리

📄 참고/특이사항
Google Cloud Service Account Key는 커밋/업로드하지 않음 (보안상 .gitignore 적용)

개발/실습 관련 문의 및 개선 제안: 이슈로 남겨주세요!

🙌 만든이
오성빈 | GitHub

주요 실습, 설계, 구현, DevOps 전과정 담당
