# 🎙️ AI TTS 기반 라디오 플랫폼

AI 음성 합성(TTS) + 웹 개발(Flask, MySQL, JavaScript, Python, HTML/CSS)로  
본인만의 라디오 방송을 만들고, AI가 안내 멘트/컨텐츠를 읽어주는 실습형 토이 프로젝트입니다.

---

## 📌 프로젝트 한눈에 보기
- **TTS 기반 라디오 플랫폼** (Google Cloud TTS *또는* 오프라인 `pyttsx3` 지원)
- **회원/인증**: JWT, 비밀번호 해시 저장(`werkzeug.security`)
- **게시판**: 목록/상세/글쓰기(서버 렌더링, Jinja2)
- **TTS로 게시글을 오디오로 재생** (웹 오디오)
- **100% 실제 동작 기반**: Flask + MySQL + Jinja2 템플릿

---

<details>
<summary><b>📁 폴더 구조 </b></summary>

```text
AI_Radio_Platform-TTS/
├── backend/                    # Flask 백엔드(REST API + 페이지 라우트)
│   ├── app.py                  # 앱 엔트리: 인증/게시판/TTS/캐시/엔진락 적용
│   ├── db.py                   # MySQL 연결
│   ├── requirements.txt        # 백엔드 의존성
│   ├── static/
│   │   └── main.css
│   └── templates/              # Jinja2 템플릿
│       ├── base.html
│       ├── index.html
│       ├── board_list.html
│       ├── board_detail.html
│       ├── write.html
│       ├── login.html
│       └── join.html
├── tools/
│   └── tts_bench.py            # 재현 가능한 TTS 벤치마크 스크립트
├── metrics/                    # 측정 결과 CSV (git에 포함)
│   └── tts_eval_pyttsx3_YYYY-mm-dd_HHMMSS.csv
├── .gitignore
└── README.md
```
</details>

---
<summary><b>🧩 주요 기능 </b></summary>

-  회원 관리: 가입/로그인(JWT), 비밀번호 해시 저장

- 게시판: 목록, 검색, 상세, 글쓰기

- AI TTS: 게시글 → 오디오(base64) 변환

- backend 파라미터로 "pyttsx3"(오프라인) / "google"(클라우드) 선택

- 파일 캐시: 텍스트 해시 기반 캐시 + 엔진 락(TTS_LOCK) 으로 동시성 안정화

- 벤치마크: tools/tts_bench.py 로 pass ratio / p50 / p95 자동 산출

<summary><b>🛠️ 기술 스택 </b></summary>

- Backend: Flask, MySQL, Jinja2, JWT, werkzeug.security

- TTS: Google Cloud Text-to-Speech, pyttsx3(오프라인)

- Frontend: HTML, CSS, JavaScript(서버 렌더링)

- ETC: dotenv, requests, tqdm

## 🔁 실행방법

### 1) 백엔드 서버
```bash
cd backend
pip install -r requirements.txt
python app.py
# http://127.0.0.1:5000
```
> 환경 변수 예시(backend/.env, 커밋 금지)

```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=*******
DB_NAME=myradio
JWT_SECRET_KEY=super-secret-key
```

### 2) 벤치마크(재현)
```bash
# 다른 터미널에서 서버가 실행 중이어야 합니다.
python tools/tts_bench.py --runs 10 --backend pyttsx3
# 결과: metrics/tts_eval_pyttsx3_YYYY-mm-dd_HHMMSS.csv
```

<summary><b>📈 개선/보완 사항 요약 </b></summary>

- **보안**: 비밀번호 평문 저장 → werkzeug.security 해시 저장/검증으로 변경

- **JWT**: 만료시간/시크릿 설정, 페이지 라우트(login_required)로 서버 렌더링 구성

- **DB 스키마**: board 테이블에 content 컬럼 추가(게시글 본문 저장)

- **TTS**:

  - 오프라인(pyttsx3) 기본값 + 엔진 단일 락/임시파일 처리로 안정성 확보

  - 텍스트 해시 기반 오디오 캐시 옵션 추가

- **측정 도구**: tools/tts_bench.py 추가(결과 CSV 자동 저장)

<summary><b>🧪 측정 결과  </b></summary>

<img width="550" height="245" alt="AI_Radio_Platform-TTS_1" src="https://github.com/user-attachments/assets/7ffbd37f-4d4c-4036-8a3e-5f2d2c734146" />

> 1차 : (p50≈109ms, p95≈263ms)

<img width="511" height="258" alt="AI_Radio_Platform-TTS_2" src="https://github.com/user-attachments/assets/08075cf7-25b0-47b5-b5d7-8b570a5fd7cc" />

> 2차 : (p50≈15.9ms)

<img width="585" height="244" alt="AI_Radio_Platform-TTS_after" src="https://github.com/user-attachments/assets/9611273b-e4e1-4404-8f8c-fd147d41c4d6" />

> 3차 : (p50≈4.28ms, p95≈101.7ms)

```ini
pass_ratio=1.000, p50=4.28ms, p95=101.73ms, n=10   # pyttsx3 (오프라인)
```

> 재현법: python tools/tts_bench.py --runs 10 --backend pyttsx3  
> CSV는 metrics/ 에 저장되어 이력과 비교가 가능합니다.

> ⚠️ 주의
> - backend/.env, Google 서비스 키 등 민감정보는 절대 커밋 금지(이미 .gitignore 포함).
> - 본 저장소는 개인 실습/포트폴리오 용도입니다. 외부 서비스 배포 전 보안 점검이 필요합니다.

🙋‍♂️ 개발: 오성빈 / GitHub: OH-SEONGBIN
