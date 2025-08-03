import React from "react";
import { Link } from "react-router-dom";

export default function MainPage() {
  return (
    <div className="main-container">
      <nav>
        <Link to="/">HOME</Link>
        <Link to="/board">BOARD</Link>
        <Link to="/login">LOGIN</Link>
        <Link to="/join">JOIN</Link>
      </nav>
      <header>
        <h1>My Radio</h1>
        <p>당신의 사연을 들려주세요.</p>
      </header>
      {/* ...이하 생략... */}
    </div>
  );
}