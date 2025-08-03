import axios from "axios";

export async function playTTS(text) {
  const res = await axios.post("http://localhost:5000/api/tts", { text });
  const audio = new Audio("data:audio/mp3;base64," + res.data.audioContent);
  audio.play();
}