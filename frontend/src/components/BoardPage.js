import React, { useState, useEffect } from "react";
import axios from "axios";
import { playTTS } from "../api/ttsClient";
import BoardWriteForm from "./BoardWriteForm";

export default function BoardPage() {
  const [list, setList] = useState([]);
  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState(null);
  const [reload, setReload] = useState(false);

  // 게시글 목록/검색
  useEffect(() => {
    axios.get("http://localhost:5000/api/board", { params: { search } })
      .then(res => setList(res.data));
  }, [search, reload]);

  // 게시글 상세
  const handleSelect = async (id) => {
    const res = await axios.get(`http://localhost:5000/api/board/${id}`);
    setSelected(res.data);
  };

  return (
    <div>
      <h2>게시판</h2>
      <form onSubmit={e => { e.preventDefault(); }}>
        <input
          value={search}
          onChange={e => setSearch(e.target.value)}
          placeholder="제목 검색"
          style={{ marginRight: 8 }}
        />
        <button type="button" onClick={() => setReload(r => !r)}>검색</button>
        <button type="button" onClick={() => setSelected({})} style={{marginLeft:10}}>글쓰기</button>
      </form>

      {/* 글쓰기 폼 */}
      {selected && selected.id === undefined && (
        <BoardWriteForm onSuccess={() => { setSelected(null); setReload(r=>!r); }} />
      )}

      {/* 게시글 상세 */}
      {selected && selected.id && (
        <div>
          <h3>{selected.title}</h3>
          <div>{selected.content}</div>
          <button onClick={() => playTTS(`${selected.title}. ${selected.content}`)}>TTS로 듣기</button>
          <button onClick={() => setSelected(null)}>목록으로</button>
        </div>
      )}

      {/* 게시글 리스트 */}
      {!selected && (
        <table>
          <thead>
            <tr>
              <th>번호</th>
              <th>제목</th>
              <th>글쓴이</th>
              <th>작성일</th>
              <th>조회</th>
            </tr>
          </thead>
          <tbody>
            {list.map(item => (
              <tr key={item.id} onClick={() => handleSelect(item.id)} style={{cursor:'pointer'}}>
                <td>{item.id}</td>
                <td>{item.title}</td>
                <td>{item.writer}</td>
                <td>{item.date && item.date.split("T")[0]}</td>
                <td>{item.views}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}