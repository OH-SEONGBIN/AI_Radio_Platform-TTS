from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from functools import wraps
from flask_cors import CORS
from db import get_connection
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta
import os, base64, tempfile


# 선택적(GCP 쓸 때만 실제 호출됨)
# from google.cloud import texttospeech

# ──────────────────────────────────────────────────────────
# 오프라인 TTS(pyɫtsx3) 준비
def synth_pyttsx3(text, fmt="wav"):
    import pyttsx3
    import tempfile, os
    eng = pyttsx3.init()
    fd, path = tempfile.mkstemp(suffix=f".{fmt}")
    os.close(fd)
    eng.save_to_file(text, path)
    eng.runAndWait()
    with open(path, "rb") as f:
        audio = f.read()
    try: os.remove(path)
    except: pass
    return audio, "audio/wav"

# ⬇️ 여기서 '지연 임포트'
def synth_google_tts(text, language="ko-KR", voice_name=None, gender="FEMALE"):
    from google.cloud import texttospeech  # 필요할 때만 임포트
    client = texttospeech.TextToSpeechClient()
    synth_input = texttospeech.SynthesisInput(text=text)
    gender_map = {
        "MALE": texttospeech.SsmlVoiceGender.MALE,
        "FEMALE": texttospeech.SsmlVoiceGender.FEMALE,
        "NEUTRAL": texttospeech.SsmlVoiceGender.NEUTRAL,
    }
    voice = texttospeech.VoiceSelectionParams(
        language_code=language,
        name=voice_name or "",
        ssml_gender=gender_map.get(gender.upper(), texttospeech.SsmlVoiceGender.FEMALE),
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    resp = client.synthesize_speech(input=synth_input, voice=voice, audio_config=audio_config)
    return resp.audio_content, "audio/mpeg"
# ──────────────────────────────────────────────────────────

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
app.secret_key = app.config['JWT_SECRET_KEY'] 
jwt = JWTManager(app)



# 회원가입
@app.route('/api/auth/join', methods=['POST'])
def join():
    data = request.get_json(force=True)
    for key in ('id', 'pw', 'name', 'birth'):
        if not data.get(key):
            return jsonify({'error': f'missing field: {key}'}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM users WHERE id=%s", (data['id'],))
            if cursor.fetchone():
                return jsonify({'error': 'id already exists'}), 409

            hashed_pw = generate_password_hash(
                data['pw'], method='pbkdf2:sha256', salt_length=16
            )
            cursor.execute(
                "INSERT INTO users (id, pw, name, birth) VALUES (%s, %s, %s, %s)",
                (data['id'], hashed_pw, data['name'], data['birth'])
            )
        conn.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# 로그인
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    if not data.get('id') or not data.get('pw'):
        return jsonify({'success': False, 'error': 'missing id or pw'}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, pw, name, birth FROM users WHERE id=%s", (data['id'],))
            user = cursor.fetchone()

        if not user or not check_password_hash(user['pw'], data['pw']):
            return jsonify({'success': False, 'error': 'invalid credentials'}), 401

        user.pop('pw', None)
        token = create_access_token(identity=user['id'])
        return jsonify({'success': True, 'token': token, 'user': user}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

# 게시글 리스트(검색 + 선택적 페이지네이션)
@app.route('/api/board', methods=['GET'])
def board_list():
    search = (request.args.get('search') or '').strip()
    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = max(int(request.args.get('offset', 0)), 0)
    except ValueError:
        return jsonify({'error': 'invalid limit/offset'}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if search:
                sql = "SELECT * FROM board WHERE title LIKE %s ORDER BY id DESC LIMIT %s OFFSET %s"
                cursor.execute(sql, (f'%{search}%', limit, offset))
            else:
                sql = "SELECT * FROM board ORDER BY id DESC LIMIT %s OFFSET %s"
                cursor.execute(sql, (limit, offset))
            rows = cursor.fetchall()
        return jsonify(rows), 200
    finally:
        conn.close()

# 게시글 상세
@app.route('/api/board/<int:board_id>', methods=['GET'])
def board_detail(board_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM board WHERE id=%s", (board_id,))
            post = cursor.fetchone()
        if not post:
            return jsonify({'error': 'not found'}), 404
        return jsonify(post), 200
    finally:
        conn.close()

# 게시글 등록
@app.route('/api/board/write', methods=['POST'])
@jwt_required()
def board_write():
    data = request.get_json(force=True)
    for key in ('title', 'content'):
        if not (data.get(key) and str(data.get(key)).strip()):
            return jsonify({'error': f'missing field: {key}'}), 400

    user_id = get_jwt_identity()
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO board (title, content, writer, date, views) VALUES (%s, %s, %s, NOW(), 0)"
            cursor.execute(sql, (data['title'], data['content'], user_id))
        conn.commit()
        return jsonify({'success': True}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

# TTS (오프라인 기본 / 요청 시 구글 사용)
@app.route('/api/tts', methods=['POST'])
def tts():
    # 안전하게 JSON 파싱
    data = request.get_json(force=True, silent=True) or {}
    text = (data.get('text') or '').strip()
    backend = (data.get('backend') or 'pyttsx3').lower()  # 기본: 오프라인 엔진

    if not text:
        return jsonify({'error': 'no text'}), 400

    try:
        if backend == 'google':
            # 필요할 때만 지연 임포트(키가 없으면 여기서만 실패)
            from google.cloud import texttospeech
            client = texttospeech.TextToSpeechClient()
            synth_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(
                language_code="ko-KR",
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
            )
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )
            resp = client.synthesize_speech(
                input=synth_input, voice=voice, audio_config=audio_config
            )
            b64 = base64.b64encode(resp.audio_content).decode('utf-8')
            return jsonify({'audioContent': b64, 'mime': 'audio/mpeg'})

        else:
            # 오프라인 TTS (Windows: SAPI5) – 과금/키 필요 없음
            import pyttsx3, tempfile, os
            fd, path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            eng = pyttsx3.init()
            eng.save_to_file(text, path)
            eng.runAndWait()
            with open(path, 'rb') as f:
                audio = f.read()
            try:
                os.remove(path)
            except:
                pass
            b64 = base64.b64encode(audio).decode('utf-8')
            return jsonify({'audioContent': b64, 'mime': 'audio/wav'})

    except Exception as e:
        # 프론트에서 alert 띄울 수 있게 메시지 반환
        return jsonify({'error': str(e)}), 500

# ───────────── 페이지용 로그인 보호 ─────────────
def login_required_page(view):
    @wraps(view)
    def _wrap(*args, **kwargs):
        if not session.get('user_id'):
            flash('로그인이 필요합니다.')
            return redirect(url_for('page_login'))
        return view(*args, **kwargs)
    return _wrap

# ───────────── 홈/메뉴 ─────────────
@app.route("/", methods=["GET"])
def index_page():
    return render_template("index.html")

# ───────────── 게시판 목록 ─────────────
@app.route("/board", methods=["GET"])
def page_board_list():
    search = (request.args.get('search') or '').strip()
    conn = get_connection()
    try:
        with conn.cursor() as c:
            if search:
                c.execute("SELECT * FROM board WHERE title LIKE %s ORDER BY id DESC", (f"%{search}%",))
            else:
                c.execute("SELECT * FROM board ORDER BY id DESC")
            rows = c.fetchall()
        return render_template("board_list.html", rows=rows, search=search)
    finally:
        conn.close()

# ───────────── 게시글 상세 ─────────────
@app.route("/board/<int:board_id>", methods=["GET"])
def page_board_detail(board_id):
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT * FROM board WHERE id=%s", (board_id,))
            post = c.fetchone()
        if not post:
            return render_template("board_detail.html", post=None), 404
        return render_template("board_detail.html", post=post)
    finally:
        conn.close()

# ───────────── 회원가입(페이지) ─────────────
@app.route("/join", methods=["GET", "POST"])
def page_join():
    if request.method == "GET":
        return render_template("join.html")
    # POST → 기존 API join 로직 재사용
    data = request.form.to_dict()
    for k in ('id','pw','name','birth'):
        if not data.get(k):
            flash(f"{k} 필드가 비었습니다.")
            return redirect(url_for('page_join'))
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT 1 FROM users WHERE id=%s", (data['id'],))
            if c.fetchone():
                flash("이미 존재하는 아이디입니다.")
                return redirect(url_for('page_join'))
            from werkzeug.security import generate_password_hash
            hashed_pw = generate_password_hash(data['pw'], method='pbkdf2:sha256', salt_length=16)
            c.execute("INSERT INTO users (id,pw,name,birth) VALUES (%s,%s,%s,%s)",
                      (data['id'], hashed_pw, data['name'], data['birth']))
        conn.commit()
        flash("회원가입 완료. 로그인 해주세요.")
        return redirect(url_for('page_login'))
    finally:
        conn.close()

# ───────────── 로그인(페이지) ─────────────
@app.route("/login", methods=["GET", "POST"])
def page_login():
    if request.method == "GET":
        return render_template("login.html")
    data = request.form.to_dict()
    if not data.get('id') or not data.get('pw'):
        flash("아이디/비밀번호를 입력하세요.")
        return redirect(url_for('page_login'))
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute("SELECT id,pw,name FROM users WHERE id=%s", (data['id'],))
            user = c.fetchone()
        from werkzeug.security import check_password_hash
        if not user or not check_password_hash(user['pw'], data['pw']):
            flash("로그인 실패: 아이디 또는 비밀번호가 올바르지 않습니다.")
            return redirect(url_for('page_login'))
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        flash("로그인 완료")
        return redirect(url_for('page_board_list'))
    finally:
        conn.close()

@app.route("/logout")
def page_logout():
    session.clear()
    flash("로그아웃 되었습니다.")
    return redirect(url_for('index_page'))

# ───────────── 글쓰기(페이지) ─────────────
@app.route("/write", methods=["GET", "POST"])
@login_required_page
def page_write():
    if request.method == "GET":
        return render_template("write.html")
    data = request.form.to_dict()
    for k in ('title','content'):
        if not data.get(k):
            flash(f"{k} 필드가 비었습니다.")
            return redirect(url_for('page_write'))
    user_id = session['user_id']
    conn = get_connection()
    try:
        with conn.cursor() as c:
            c.execute("INSERT INTO board (title, content, writer, date, views) VALUES (%s,%s,%s,NOW(),0)",
                      (data['title'], data['content'], user_id))
        conn.commit()
        flash("등록되었습니다.")
        return redirect(url_for('page_board_list'))
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)