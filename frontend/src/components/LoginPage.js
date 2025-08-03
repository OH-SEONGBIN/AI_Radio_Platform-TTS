import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [id, setId] = useState("");
  const [pw, setPw] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const res = await axios.post("http://localhost:5000/api/auth/login", {
        id,
        pw,
      });
      if (res.data.success) {
        localStorage.setItem("token", res.data.token);
        localStorage.setItem("userId", res.data.user.id);
        alert("로그인 성공!");
        navigate("/");
      }
    } catch {
      alert("로그인 실패!");
    }
  };

  return (
    <div className="login-container">
      <h2>Log-in</h2>
      <input
        type="text"
        placeholder="ID"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <input
        type="password"
        placeholder="PW"
        value={pw}
        onChange={(e) => setPw(e.target.value)}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}