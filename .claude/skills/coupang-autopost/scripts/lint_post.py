#!/usr/bin/env python3
"""게시물 검수. 사용: python3 lint_post.py post.json
post.json: {"threads":["1번글","2번글(링크)"], "instagram":"캡션"}  (없는 채널은 생략)
통과 시 exit 0, 실패 시 사유 출력 후 exit 1.
"""
import json, re, sys, pathlib

cfg = json.load(open(pathlib.Path(__file__).parent.parent / "config.json", encoding="utf-8"))
DISC = "쿠팡 파트너스"
LIMIT = {"threads": 500, "instagram": 2200}
BAD = ["최저가 보장", "무조건", "100% 효과", "완치", "치료", "기적", "대방출", "알아보겠습니다", "결론적으로"]
LINK = re.compile(r"link\.coupang\.com|coupa\.ng|coupang\.com")
errs = []
d = json.load(open(sys.argv[1], encoding="utf-8"))

def chk(ch, text, need_disc):
    if len(text) > LIMIT[ch]: errs.append(f"{ch}: {len(text)}자 > {LIMIT[ch]}")
    for b in BAD:
        if b in text: errs.append(f"{ch}: 금지/AI투 표현 '{b}'")
    if len(re.findall(r"[\U0001F300-\U0001FAFF]", text)) > 2: errs.append(f"{ch}: 이모지 과다")
    if re.search(r"[0-9,]+\s*원", text): errs.append(f"{ch}: 가격 단정 금지(링크에서 확인으로)")
    if need_disc and DISC not in text: errs.append(f"{ch}: 대가성 문구 누락")
    if LINK.search(text) and DISC not in text: errs.append(f"{ch}: 링크가 있는데 대가성 문구 없음")

for i, t in enumerate(d.get("threads", [])):
    chk("threads", t, need_disc=bool(LINK.search(t)))
if d.get("threads") and not any(LINK.search(t) for t in d["threads"]): errs.append("threads: 링크 없음")
if "instagram" in d: chk("instagram", d["instagram"], need_disc=True)
if d.get("threads") and LINK.search(d["threads"][0]): errs.append("threads: 1번 글에 링크 금지(답글로)")

print("\n".join(errs) if errs else "OK")
sys.exit(1 if errs else 0)
