#!/usr/bin/env python3
"""글을 담은 열기 링크를 만든다 (내용은 URL # 뒤에만 들어가 서버로 전송되지 않는다).

사용: python3 make_link.py post.json [기본주소]
post.json: {"t": "제목", "b": "본문 마크다운", "g": ["태그", ...], "c": "카테고리명"}
"""
import base64, json, sys, zlib

BASE = "https://godjy2.github.io/promo_mngr/blog-mobile/"
d = json.load(open(sys.argv[1], encoding="utf-8"))
raw = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
c = zlib.compressobj(9, zlib.DEFLATED, -15)
z = c.compress(raw) + c.flush()
print((sys.argv[2] if len(sys.argv) > 2 else BASE) + "#d=" + base64.urlsafe_b64encode(z).rstrip(b"=").decode())
