import React, { useState } from "react";
import axios from "axios";

function getToken() { return localStorage.getItem("token"); }

export default function BoardWriteForm({ onSuccess }) {
  const [form, setForm] = useState({ title: "", content: "" });

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    if (!getToken()) {
      alert("로그인 후 작성 가능합니다.");
      return;
    }
    await axios.post("http://localhost:5000/api/board/write", form, {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    alert("등록 완료!");
    onSuccess();
  };

  return (
    <form onSubmit={handleSubmit} style={{margin:'16px 0'}}>
      <input name="title" value={form.title} onChange={handleChange} placeholder="제목" required /><br />
      <textarea name="content" value={form.content} onChange={handleChange} placeholder="내용" required /><br />
      <button type="submit">등록</button>
      <button type="button" onClick={onSuccess} style={{marginLeft:8}}>취소</button>
    </form>
  );
}