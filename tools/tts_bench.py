import argparse, csv, os, time, datetime
import requests
import statistics as stats


import argparse, csv, os, time, datetime
import requests

API = os.environ.get("API_BASE", "http://127.0.0.1:5000")

SAMPLE_TEXT = "안녕하세요. 인공지능 라디오 데모 입니다. 게시글 내용을 음성으로 변환합니다."

def bench(runs: int, backend: str):
    os.makedirs("metrics", exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out = f"metrics/tts_eval_{backend}_{ts}.csv"

    rows = []
    oks = 0
    latencies = []

    for i in range(runs):
        t0 = time.perf_counter()
        try:
            r = requests.post(f"{API}/api/tts", json={"text": SAMPLE_TEXT, "backend": backend}, timeout=60)
            elapsed = (time.perf_counter() - t0) * 1000.0
            ok = r.ok
            audio_len = 0
            if ok:
                j = r.json()
                audio_b64 = j.get("audioContent", "")
                audio_len = len(audio_b64)
                ok = ok and (audio_len > 0)
            else:
                j = {}
            rows.append({
                "i": i+1,
                "backend": backend,
                "latency_ms": round(elapsed, 2),
                "audio_b64_len": audio_len,
                "status": r.status_code,
                "ok": ok,
                "err": ("" if ok else str(j.get("error") or r.text)[:200])
            })
            if ok:
                oks += 1
                latencies.append(elapsed)
            print(f"[{i+1}/{runs}] {backend} {elapsed:.2f}ms ok={ok} len={audio_len}")
        except Exception as e:
            elapsed = (time.perf_counter() - t0) * 1000.0
            rows.append({"i": i+1, "backend": backend, "latency_ms": round(elapsed,2),
                         "audio_b64_len": 0, "status": 0, "ok": False, "err": str(e)[:200]})
            print(f"[{i+1}/{runs}] {backend} ERROR: {e}")

    # save
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # summary
    latencies.sort()
    def pct(p):
        if not latencies: return None
        k = max(0, min(len(latencies)-1, int(round((p/100.0)*(len(latencies)-1)))))
        return latencies[k]

    p50 = pct(50)
    p95 = pct(95)
    pass_ratio = (oks / runs) if runs else 0.0

    print(f"[OK] saved: {out}")
    print(f"pass_ratio={pass_ratio:.3f}, p50={p50:.2f}ms, p95={p95:.2f}ms, n={runs}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=10)
    ap.add_argument("--backend", choices=["pyttsx3","google"], default="pyttsx3")
    args = ap.parse_args()
    bench(args.runs, args.backend)