from flask import Flask, request, jsonify
from flask_cors import CORS
from db import get_connection
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
import os
from google.cloud import texttospeech
import base64

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
jwt = JWTManager(app)

# 회원가입
@app.route('/api/auth/join', methods=['POST'])
def join():
    data = request.json
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (id, pw, name, birth) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (data['id'], data['pw'], data['name'], data['birth']))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()

# 로그인
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE id=%s AND pw=%s"
            cursor.execute(sql, (data['id'], data['pw']))
            user = cursor.fetchone()
            if user:
                token = create_access_token(identity=user['id'])
                return jsonify({'success': True, 'token': token, 'user': user})
            else:
                return jsonify({'success': False}), 401
    finally:
        conn.close()

# 게시글 리스트(검색)
@app.route('/api/board', methods=['GET'])
def board_list():
    search = request.args.get('search', '')
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if search:
                sql = "SELECT * FROM board WHERE title LIKE %s ORDER BY id DESC"
                cursor.execute(sql, (f'%{search}%',))
            else:
                sql = "SELECT * FROM board ORDER BY id DESC"
                cursor.execute(sql)
            rows = cursor.fetchall()
        return jsonify(rows)
    finally:
        conn.close()

# 게시글 상세
@app.route('/api/board/<int:board_id>', methods=['GET'])
def board_detail(board_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM board WHERE id=%s"
            cursor.execute(sql, (board_id,))
            post = cursor.fetchone()
        return jsonify(post)
    finally:
        conn.close()

# 게시글 등록
@app.route('/api/board/write', methods=['POST'])
@jwt_required()
def board_write():
    data = request.json
    user_id = get_jwt_identity()
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO board (title, content, writer, date, views) VALUES (%s, %s, %s, NOW(), 0)"
            cursor.execute(sql, (data['title'], data['content'], user_id))
        conn.commit()
        return jsonify({'success': True})
    finally:
        conn.close()

# TTS (제목+내용 읽어주기)
@app.route('/api/tts', methods=['POST'])
def tts():
    text = request.json.get('text')
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    audio_content = base64.b64encode(response.audio_content).decode('utf-8')
    return jsonify({'audioContent': audio_content})

if __name__ == '__main__':
    app.run(debug=True, port=5000)