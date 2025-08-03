# 🎙️ AI TTS 기반 라디오 플랫폼

AI 음성 합성(TTS) + 웹 개발(Flask, MySQL, JavaScript, Python, HTML/CSS)  
본인만의 라디오 방송을 만들고, AI가 안내멘트/컨텐츠를 읽어주는 실습형 토이 프로젝트입니다.

---

## 📌 프로젝트 한눈에 보기

- **TTS 기반 라디오 플랫폼** (Google Cloud TTS 등 실제 API 연동)
- **주요 기능**
  - 회원가입/로그인/인증, 게시판/채팅
  - AI TTS로 라디오 방송 생성
  - 여러 테마(카테고리)별 방송
- **100% 실제 구현 기반:**  
  - Flask + MySQL + JavaScript + Python + HTML/CSS

---


## 🗂️ 폴더 구조

```plaintext
├── backend/         # Python FastAPI(Flask) TTS/REST API
├── frontend/        # React/Vue/HTML SPA UI
├── requirements.txt # 백엔드 의존성
├── .gitignore
├── README.md

```

🚦 주요 기능
- 회원 관리(회원가입/로그인/로그아웃)

- 게시판 검색 및 등록

- AI TTS를 활용한 라디오 컨텐츠 생성

- 방송별 카테고리 분류 및 리스트 뷰



⚙️ 기술 스택
| 구분    | 기술                                   |
| ----- | ------------------------------------ |
| 백엔드   | Flask, Python, MySQL, Google TTS API |
| 프론트엔드 | HTML, CSS, JavaScript                |
| 기타    | Jinja2, AJAX, .gitignore             |



🚀 실행 방법
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
```

📝 실습/포트폴리오 주요 학습 내용
- TTS+웹서비스 아키텍처 경험

- 보안 민감정보 커밋방지(.gitignore) 실습

- 실무 프로젝트 구조 직접 설계/구현/배포

📸 대표 UI (스크린샷/링크)
<img width="1043" height="538" alt="_" src="https://github.com/user-attachments/assets/b0c7cce3-bba8-4810-852b-b4cb2d493c4c" />

<img width="1621" height="747" alt="5" src="https://github.com/user-attachments/assets/45319cc2-1338-47fe-a882-40be54bedbfa" />

🛡️ 주의사항 및 보안 정책
- Google Cloud 서비스키 등 민감정보는 .gitignore로 반드시 보호

- 개인 실습/포트폴리오용으로만 활용 (외부 서비스 배포 전 별도 보안 점검 필요)

🙋‍♂️ 개발/실습: 오성빈
- 깃허브: OH-SEONGBIN

- 추가 질문/참여/리뷰는 이슈로 남겨주세요!
