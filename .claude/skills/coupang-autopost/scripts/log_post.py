#!/usr/bin/env python3
"""발행 기록 + 중복 확인. 사용: log_post.py check <링크>  |  log_post.py add <링크> <채널> <예약시각>"""
import json, sys, time, pathlib
f = pathlib.Path(__file__).parent.parent / "posted.jsonl"
cfg = json.load(open(f.parent / "config.json", encoding="utf-8"))
rows = [json.loads(l) for l in f.read_text(encoding="utf-8").splitlines()] if f.exists() else []
if sys.argv[1] == "check":
    recent = [r for r in rows if r["link"] == sys.argv[2] and time.time() - r["ts"] < cfg["dedupeDays"] * 86400]
    print("DUP" if recent else "NEW"); sys.exit(1 if recent else 0)
with f.open("a", encoding="utf-8") as o:
    o.write(json.dumps({"link": sys.argv[2], "channel": sys.argv[3], "at": sys.argv[4], "ts": time.time()}, ensure_ascii=False) + "\n")
