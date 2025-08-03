import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function JoinPage() {
  const [form, setForm] = useState({ id: "", pw: "", name: "", birth: "" });
  const navigate = useNavigate();

  const handleChange = e =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleJoin = async () => {
    await axios.post("http://localhost:5000/api/auth/join", form);
    alert("회원가입 완료!");
    navigate("/login");
  };

  return (
    <div className="join-container">
      <h2>JOIN</h2>
      <input name="id" placeholder="ID" onChange={handleChange} />
      <input
        name="pw"
        type="password"
        placeholder="PW"
        onChange={handleChange}
      />
      <input name="name" placeholder="NAME" onChange={handleChange} />
      <input name="birth" placeholder="BIRTH" onChange={handleChange} />
      <button onClick={handleJoin}>Join</button>
    </div>
  );
}