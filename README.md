🎙️ AI TTS 기반 라디오 플랫폼

AI 음성 합성(TTS) + 웹 개발(Flask, MySQL, JavaScript, Python, HTML/CSS)
본인만의 라디오 방송을 만들고, AI가 안내 멘트/컨텐츠를 읽어주는 실습형 토이 프로젝트입니다.

📌 프로젝트 한눈에 보기

TTS 기반 라디오 플랫폼 (Google Cloud TTS 또는 오프라인 pyttsx3 지원)

주요 기능

회원가입/로그인/인증(JWT, 비밀번호 해시 저장)

게시판(검색/상세/글쓰기)

AI TTS로 게시글 내용을 웹 오디오로 재생

실제 동작 기반

백엔드: Flask + MySQL + Jinja2

프런트: 서버 렌더링(HTML/CSS/JS)

벤치마크 스크립트 + CSV 측정 결과 포함(재현 가능)

🗂️ 폴더 구조
AI_Radio_Platform-TTS/
├── backend/                  # Flask 백엔드(TTS/REST API + 페이지 라우트)
│   ├── app.py                # 인증/게시판/TTS/페이지 라우트 + 캐시/엔진락 적용
│   ├── db.py                 # MySQL 연결
│   ├── requirements.txt      # 백엔드 의존성
│   ├── static/
│   │   └── main.css
│   └── templates/            # Jinja2 템플릿
│       ├── base.html  ├── index.html  ├── board_list.html
│       ├── board_detail.html ├── write.html
│       ├── login.html        └── join.html
├── tools/
│   └── tts_bench.py          # 재현 가능한 TTS 벤치마크 스크립트
├── metrics/                  # 측정 결과 CSV (git에 포함)
│   ├── tts_eval_pyttsx3_YYYY-mm-dd_HHMMSS.csv
│   └── ...
├── .gitignore
└── README.md


예전 SPA용 frontend/는 현재 사용하지 않습니다(서버 렌더링으로 대체). 남아 있다면 정리하거나 사용 계획을 명시하세요.

🚦 주요 기능

회원 관리: 가입/로그인(JWT), 비밀번호 해시 저장

게시판: 목록 검색, 상세, 글쓰기(JWT 필요)

AI TTS: /api/tts 로 텍스트 → 오디오(base64) 변환

backend: "pyttsx3" | "google" 선택

파일 캐시 + 엔진 락 + 워밍업 적용(지연시간 안정화)

⚙️ 기술 스택

Backend: Flask, MySQL, Jinja2, JWT, werkzeug.security

TTS: Google Cloud Text-to-Speech, pyttsx3(오프라인)

Frontend: HTML, CSS, JavaScript(서버 렌더링)

Etc.: .env, requests, tqdm

🚀 실행 방법
1) 의존성 설치
# 프로젝트 루트
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows PowerShell
python -m pip install -U pip
pip install -r backend/requirements.txt

2) 환경 변수(.env) 설정 　※ 레포에 커밋 금지

backend/.env

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=myradio
JWT_SECRET_KEY=super-secret-key

# (선택) Google TTS 사용 시
# GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json

3) 서버 실행
# 리로더 OFF(벤치할 때 권장)
$Env:FLASK_APP="backend.app:app"
flask run --host 127.0.0.1 --port 5000 --no-reload


브라우저: http://127.0.0.1:5000
홈/로그인/게시판/상세/TTS 버튼을 순서대로 확인하세요.

🔬 벤치마크(재현 가능)

tools/tts_bench.py 로 동일 텍스트를 여러 번 호출해 성공률/지연시간을 CSV로 저장합니다.

# 서버가 127.0.0.1:5000 에 떠 있는 상태에서 실행
python tools/tts_bench.py --runs 10 --backend pyttsx3
# (선택) Google TTS
python tools/tts_bench.py --runs 10 --backend google


결과 파일: metrics/tts_eval_<backend>_YYYY-mm-dd_HHMMSS.csv

워밍업 1회 후 캐시가 잡혀 지연시간이 크게 감소합니다. 더 깔끔한 지표를 원하면 첫 샘플을 제외하거나 --runs 20으로 늘리세요.

📊 측정 예시(실제 실행값)
구분	pass ratio	p50	p95	비고
Before(강제 캐시 미스/락 없음)	0.10	≈ 60,004ms	≈ 60,027ms	10회 중 9회 타임아웃
After(파일 캐시 + 엔진 락 적용)	1.00	≈ 4.28ms	≈ 101.73ms	워밍업 1회 + 캐시 히트

개선 효과: 성공률 +90pp(0.10→1.00), p50 -99.99%, p95 -99.8%.
CSV는 metrics/ 폴더에 포함되어 있어 재현 가능한 성과로 제출할 수 있습니다.

🛡️ 보안 & 운영 메모

비밀번호 평문 저장 금지 → generate_password_hash / check_password_hash

.env / 서비스키(json) 절대 커밋 금지 → .gitignore에 포함

Google TTS는 유료/쿼터 이슈가 있어, 기본은 오프라인(pyTTSx3) 로 제공

Windows의 pyttsx3는 SAPI5 엔진(첫 호출 워밍업 주의)

.gitignore (요지)

.env
__pycache__/
*.pyc
.venv/
venv/
*.json

🧪 수동 테스트

회원가입 → 로그인 → 글쓰기(제목/내용)

상세 페이지에서 “이 사연 듣기(TTS)” 클릭 → 오디오 플레이

개발자도구 Network에서 /api/tts 응답(base64, mime) 확인

🛠 트러블슈팅

ModuleNotFoundError: No module named 'google' → 패키지 이름은 google-cloud-texttospeech

ERR_CONNECTION_REFUSED → 서버 포트/실행 여부 확인

루트 / 404 → 페이지 라우트/템플릿 경로 확인

MySQL 연결 불가 → .env의 DB 설정/계정/포트 점검

🙋‍♂️ 개발/실습

오성빈 · GitHub: OH-SEONGBIN

질문/리뷰/기여는 Issues 또는 Pull Request로 남겨주세요!
