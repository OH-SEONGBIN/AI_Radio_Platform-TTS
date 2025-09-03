🎙️ AI TTS 기반 라디오 플랫폼

AI 음성 합성(TTS) + 웹 개발(Flask, MySQL, JavaScript, Python, HTML/CSS)
본인만의 라디오 방송을 만들고, AI가 안내멘트/컨텐츠를 읽어주는 실습형 토이 프로젝트입니다.

📌 프로젝트 한눈에 보기

TTS 기반 라디오 플랫폼 (Google Cloud TTS 또는 오프라인 pyttsx3 지원)

주요 기능

회원가입/로그인/인증(JWT, 비밀번호 해시 저장)

게시판(검색/상세/글쓰기)

AI TTS로 게시글 내용을 음성으로 재생(웹 오디오)

100% 실제 구현 기반

백엔드: Flask + MySQL + Jinja2 템플릿

프런트: 서버 렌더링(HTML/CSS/JS)

벤치마크 스크립트와 CSV 측정 결과 포함(재현 가능)

🗂️ 폴더 구조
AI_Radio_Platform-TTS/
├── backend/                  # Flask 백엔드(TTS/REST API + 페이지 라우트)
│   ├── app.py                # 앱 엔트리: 인증/게시판/TTS/페이지 라우트
│   ├── db.py                 # MySQL 연결
│   ├── requirements.txt      # 백엔드 의존성
│   ├── static/
│   │   └── main.css
│   └── templates/            # Jinja2 템플릿(서버 렌더링)
│       ├── base.html
│       ├── index.html
│       ├── board_list.html
│       ├── board_detail.html
│       ├── write.html
│       ├── login.html
│       └── join.html
├── tools/
│   └── tts_bench.py          # 재현 가능한 TTS 벤치마크 스크립트
├── metrics/                  # 측정 결과 CSV (git에 포함)
│   ├── tts_eval_pyttsx3_YYYY-mm-dd_HHMMSS.csv
│   └── ...
├── .gitignore
└── README.md


참고: 예전 SPA용 frontend/는 현재 사용하지 않습니다(서버 렌더링으로 대체). 폴더가 남아있다면 정리하거나 사용 계획을 README에 명시하세요.

🚦 주요 기능

회원 관리

회원가입(비밀번호 해시 저장: werkzeug.security.generate_password_hash)

로그인(JWT 발급), 로그아웃

게시판

목록 검색(GET /api/board?search=...)

상세 조회(GET /api/board/<id>)

글쓰기(POST /api/board/write, JWT 필요)

AI TTS

POST /api/tts로 텍스트를 음성 파일로 변환

백엔드 선택: pyttsx3(오프라인) / google(Google Cloud TTS)

파일 캐시 + 엔진 락 적용으로 지연시간 안정화

🔗 API & 페이지 라우트
API

POST /api/auth/join
Body: {"id": "...", "pw": "...", "name": "...", "birth": "YYYY-MM-DD"}
응답: {"success":true}

POST /api/auth/login
Body: {"id":"...", "pw":"..."}
응답: {"success":true,"token":"<JWT>","user":{...}}

GET /api/board?search=키워드
응답: 게시글 배열

GET /api/board/<id>
응답: 게시글 단건

POST /api/board/write (JWT 필요)
Header: Authorization: Bearer <JWT>
Body: {"title":"...", "content":"..."}

POST /api/tts
Body:

{
  "text": "안녕하세요",
  "backend": "pyttsx3",   // 또는 "google"
  "cache": true           // (선택) 캐시 사용
}


응답: {"audioContent":"<base64>","mime":"audio/wav|audio/mpeg"}

페이지(View)

GET / 홈

GET /board 목록

GET /board/<id> 상세+TTS 버튼

GET /write 글쓰기(로그인 필요)

GET /login, GET /join

🗄️ DB 스키마
CREATE DATABASE myradio DEFAULT CHARACTER SET utf8mb4;
USE myradio;

CREATE TABLE users (
  id    VARCHAR(30) PRIMARY KEY,
  pw    VARCHAR(255),      -- 해시 저장
  name  VARCHAR(50),
  birth VARCHAR(20)
);

CREATE TABLE board (
  id      INT AUTO_INCREMENT PRIMARY KEY,
  title   VARCHAR(200),
  content TEXT,
  writer  VARCHAR(50),
  date    DATETIME,
  views   INT
);

⚙️ 기술 스택
구분	기술
백엔드	Flask, Python, MySQL, Jinja2, JWT, werkzeug.security
TTS	Google Cloud Text-to-Speech, pyttsx3(오프라인)
프론트	HTML/CSS/JavaScript(서버 렌더링)
기타	.gitignore, dotenv, requests, tqdm
🚀 실행 방법
0) 의존성 설치
# 프로젝트 루트
python -m venv .venv
.\.venv\Scripts\Activate.ps1        # Windows PowerShell
python -m pip install -U pip

# 백엔드 패키지 설치
pip install -r backend/requirements.txt


backend/requirements.txt (예시)

flask
flask-cors
pymysql
flask-jwt-extended
google-cloud-texttospeech
python-dotenv
werkzeug>=3.0.1
requests>=2.31.0
tqdm>=4.66.0
pyttsx3>=2.90
pywin32>=306; sys_platform == "win32"

1) 환경변수(.env) 설정 (레포에 커밋 금지)

backend/.env

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=비밀번호
DB_NAME=myradio

JWT_SECRET_KEY=super-secret-key

# (선택) Google TTS 사용 시
# GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\service-account.json

2) 서버 실행
# 루트에서
$Env:FLASK_APP="backend.app:app"
flask run --host 127.0.0.1 --port 5000 --no-reload   # 리로더 OFF 권장


브라우저에서 http://127.0.0.1:5000 접속 → 홈/로그인/게시판/상세/TTS 사용

🔬 재현 가능한 TTS 벤치마크

tools/tts_bench.py 스크립트로 동일한 텍스트에 대해 여러 번 요청하여 성공률/지연시간을 CSV로 저장합니다.

# 1) 서버(리로더 OFF)
$Env:FLASK_APP="backend.app:app"
flask run --host 127.0.0.1 --port 5000 --no-reload

# 2) 벤치마크 (기본: 오프라인 pyttsx3)
python tools/tts_bench.py --runs 10 --backend pyttsx3

# 3) (선택) Google TTS
python tools/tts_bench.py --runs 10 --backend google


결과 CSV는 metrics/tts_eval_<backend>_YYYY-mm-dd_HHMMSS.csv로 저장됩니다.

첫 요청은 워밍업으로 비교적 큰 지연이 나올 수 있습니다(캐시 생성).
좀 더 깔끔한 지표를 원하면 워밍업 1회 후 측정하거나(첫 샘플 제외), runs를 20으로 늘려서 통계적 안정성을 확보하세요.

📊 측정 예시 (실제 수치)
구분	pass ratio	p50	p95	비고
Before (캐시/락 없이 강제 미스)	0.10	≈ 60,016ms	≈ 60,027ms	10회 중 9회 실패(타임아웃)
After (파일 캐시 + 엔진 락 적용)	1.00	≈ 4.28ms	≈ 101.73ms	1회 워밍업 + 9회 캐시 히트

개선 효과: 성공률 +90pp(0.10→1.00), p50 -99.99%, p95 -99.8%.
CSV는 metrics/ 폴더에 함께 커밋되어 재현 가능합니다.

🔐 보안 & 운영 메모

비밀번호는 평문 저장 금지 → generate_password_hash / check_password_hash 사용

.env / 서비스키(json)는 절대 커밋 금지 → .gitignore에 포함

Google TTS는 요금/쿼터가 있으므로, **오프라인(pyTTSx3)**를 기본으로 제공

Windows에서 pyttsx3는 SAPI5 엔진 사용(첫 호출은 워밍업 필요)

.gitignore(요지)

.env
__pycache__/
*.pyc
log_langchain.csv
venv/
.venv/
*.json

🧪 수동 테스트 팁

회원가입 → 로그인 → 글쓰기(제목/내용)

상세 페이지에서 “이 사연 듣기(TTS)” 버튼 클릭 → 오디오 재생

개발자 콘솔(Network)에서 /api/tts 응답 확인(오디오 base64, mime)

🛠️ 트러블슈팅

ModuleNotFoundError: No module named 'google'
→ google-cloud-texttospeech를 설치하세요. 패키지 이름이 google이 아닙니다.

ERR_CONNECTION_REFUSED
→ 서버가 내려갔거나 포트가 다릅니다. flask run --port 5000 --no-reload로 재실행.

루트 /에서 404
→ index_page() 라우트가 있는지 확인(템플릿/파일 경로 포함).

MySQL 연결 오류
→ .env DB 설정과 로컬 MySQL 계정/비밀번호/포트를 확인하세요.

📝 실습/포트폴리오 주요 학습 내용

TTS + 웹서비스 아키텍처(API/페이지 혼합) 설계/구현

보안: JWT 인증, 비밀번호 해시 저장, 비밀정보 커밋 방지

성능 개선: pyttsx3 파일 캐시 + 엔진 락 + 워밍업 적용으로 지연시간 99%+ 절감

재현성: 벤치마크 스크립트/CSV 포함으로 측정 → 개선 → 검증 루프 구축

📸 대표 UI (예시)

홈, 게시판 목록/상세, 로그인/가입, 글쓰기, 상세에서 TTS 버튼 + 오디오 플레이어
(스크린샷은 docs/ 또는 이 README에 이미지로 첨부 가능)

🙋‍♂️ 개발/실습

오성빈 (GitHub: OH-SEONGBIN
)

질문/리뷰/기여는 Issues 또는 Pull Request로 남겨주세요.