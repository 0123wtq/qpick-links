#!/usr/bin/env python3
"""큐픽 링크모음 페이지 빌더.

products.json 하나만 고치고 이 스크립트를 실행하면 index.html이 다시 만들어집니다.
    python3 build.py
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
DATA = json.loads((ROOT / "products.json").read_text(encoding="utf-8"))

E = html.escape

PLAY_ICON = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'
    '<path d="M9 7.5v9a1 1 0 0 0 1.53.85l6.5-4.5a1 1 0 0 0 0-1.7l-6.5-4.5A1 1 0 0 0 9 7.5z"/>'
    "</svg>"
)
LINK_ICON = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M10 13a5 5 0 0 0 7.1 0l2-2a5 5 0 0 0-7.1-7.1l-1 1"/>'
    '<path d="M14 11a5 5 0 0 0-7.1 0l-2 2A5 5 0 0 0 12 20.1l1-1"/></svg>'
)
ARROW_ICON = (
    '<svg class="arw" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
    'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M7 17 17 7M9 7h8v8"/></svg>'
)
BAG_ICON = (
    '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M6 8h12l-1 12H7L6 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>'
)

LINK_ICONS = {
    "threads": '<span class="glyph">@</span>',
    "blog": '<span class="glyph">N</span>',
    "chat": (
        '<svg class="ico" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M20 12a7.5 7.5 0 0 1-7.5 7.5c-1.2 0-2.4-.3-3.4-.8L4.5 20l1.3-4A7.4 7.4 0 0 1 5 12a7.5 7.5 0 0 1 15 0z"/>'
        "</svg>"
    ),
}
DEFAULT_LINK_ICON = LINK_ICON


def card(p: dict, index: int) -> str:
    num = p.get("id") or f"{index + 1:02d}"
    cat = p.get("category", "")
    emoji = p.get("emoji", "")
    parts = [
        '<article class="card">',
        '  <div class="card-head">',
        f'    <span class="num">#{E(num)}</span>',
    ]
    if cat:
        parts.append(f'    <span class="cat">{E(cat)}</span>')
    if emoji:
        parts.append(f'    <span class="emoji" aria-hidden="true">{E(emoji)}</span>')
    parts += [
        "  </div>",
        f'  <h2 class="name">{E(p["name"])}</h2>',
    ]
    if p.get("option"):
        parts.append(f'  <p class="opt">{E(p["option"])}</p>')
    if p.get("hook"):
        parts.append(f'  <p class="hook">{E(p["hook"])}</p>')
    if p.get("price"):
        price = ['  <div class="price">', f'    <span class="sale">{E(p["price"])}</span>']
        if p.get("original_price"):
            price.append(f'    <span class="was">{E(p["original_price"])}</span>')
        if p.get("discount"):
            price.append(f'    <span class="off">{E(p["discount"])}</span>')
        price.append("  </div>")
        parts += price
    main = p.get("main") or {}
    if main.get("url"):
        parts.append(
            f'  <a class="btn btn-main" href="{E(main["url"], quote=True)}" target="_blank" '
            f'rel="sponsored noopener noreferrer">{BAG_ICON}<span>{E(main.get("label", "상품 보기"))}</span></a>'
        )
    for s in p.get("sub") or []:
        icon = PLAY_ICON if s.get("icon") == "play" else LINK_ICON
        parts.append(
            f'  <a class="btn btn-sub" href="{E(s["url"], quote=True)}" target="_blank" '
            f'rel="noopener noreferrer">{icon}<span>{E(s.get("label", "영상 보기"))}</span></a>'
        )
    parts.append("</article>")
    return "\n".join("    " + line if line else line for line in "\n".join(parts).split("\n"))


def link_pill(item: dict) -> str:
    icon = LINK_ICONS.get(item.get("icon", ""), DEFAULT_LINK_ICON)
    return (
        '    <a class="pill" href="{url}" target="_blank" rel="noopener noreferrer">'
        '<span class="pill-label">{icon}<span>{label}</span></span>{arrow}</a>'
    ).format(
        url=E(item["url"], quote=True),
        icon=icon,
        label=E(item["label"]),
        arrow=ARROW_ICON,
    )


CSS = """
  :root{
    --bg:#FBF7F1; --card:#FFFFFF; --ink:#241F1A; --body:#574E45; --muted:#8E8276;
    --line:#EFE6DA; --accent:#DF5537; --accent-d:#C6472B; --soft:#FCEAE2;
  }
  *,*::before,*::after{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
  html{-webkit-text-size-adjust:100%}
  body{
    margin:0;color:var(--ink);
    background:radial-gradient(125% 55% at 50% 0%, #FFF2E8 0%, #FBF7F1 58%) no-repeat;
    background-color:#FBF7F1;
    font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Pretendard","Malgun Gothic",system-ui,sans-serif;
    line-height:1.5;-webkit-font-smoothing:antialiased;
    padding:calc(34px + env(safe-area-inset-top)) 20px calc(30px + env(safe-area-inset-bottom));
    word-break:keep-all;
  }
  .wrap{max-width:480px;margin:0 auto}
  header{display:block}
  .brand{display:flex;align-items:baseline;gap:7px;margin:0}
  .brand b{font-size:15px;font-weight:800;letter-spacing:.01em}
  .brand .en{font-size:10.5px;font-weight:700;letter-spacing:.2em;color:var(--muted)}
  .brand .dot{color:var(--soft-d, #D9CFC2);font-weight:700}
  h1{font-size:26px;line-height:1.35;font-weight:800;letter-spacing:-.035em;margin:13px 0 0}
  h1 .hl{color:var(--accent)}
  .intro{font-size:13px;line-height:1.6;color:var(--muted);margin:9px 0 0}
  main{margin-top:20px}
  .card{
    background:var(--card);border:1px solid var(--line);border-radius:22px;
    padding:17px 17px 15px;margin:0 0 13px;
    box-shadow:0 3px 16px rgba(74,52,30,.05);
  }
  .card-head{display:flex;align-items:center;gap:9px;min-height:24px}
  .num{font-size:11.5px;font-weight:800;letter-spacing:.03em;color:var(--accent);background:var(--soft);padding:4px 9px;border-radius:999px}
  .cat{font-size:11.5px;font-weight:700;color:var(--muted)}
  .emoji{margin-left:auto;font-size:19px;line-height:1;opacity:.95}
  .name{font-size:17.5px;line-height:1.38;font-weight:800;letter-spacing:-.025em;margin:11px 0 0}
  .opt{font-size:11.5px;color:var(--muted);margin:4px 0 0;letter-spacing:-.01em}
  .hook{font-size:13.5px;line-height:1.55;color:var(--body);margin:9px 0 0}
  .price{display:flex;align-items:baseline;gap:7px;margin:13px 0 0;flex-wrap:wrap}
  .sale{font-size:19px;font-weight:800;letter-spacing:-.03em}
  .was{font-size:12px;color:#B6AB9F;text-decoration:line-through}
  .off{font-size:11px;font-weight:800;color:var(--accent);background:var(--soft);padding:2px 6px;border-radius:6px}
  .btn{
    display:flex;align-items:center;justify-content:center;gap:7px;
    height:52px;border-radius:15px;font-size:15.5px;font-weight:800;letter-spacing:-.02em;
    text-decoration:none;margin-top:15px;
  }
  .btn .ico{width:17px;height:17px;flex:none}
  .btn-main{background:var(--accent);color:#fff;box-shadow:0 6px 16px rgba(223,85,55,.22)}
  .btn-main:active{background:var(--accent-d);transform:translateY(1px)}
  .btn-sub{height:46px;margin-top:8px;background:#fff;color:#4A4038;border:1px solid var(--line);font-size:14.5px;font-weight:700}
  .btn-sub:active{background:#FBF7F1}
  .btn-sub .ico{color:var(--accent)}
  .links{margin:22px 0 0;display:grid;gap:8px}
  .pill{
    display:flex;align-items:center;justify-content:space-between;gap:10px;
    height:48px;padding:0 15px;background:#fff;border:1px solid var(--line);border-radius:14px;
    text-decoration:none;color:#3E362E;font-size:13.5px;font-weight:700;letter-spacing:-.01em;
  }
  .pill:active{background:#FBF7F1}
  .pill-label{display:flex;align-items:center;gap:9px;min-width:0}
  .pill-label span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .pill .ico{width:16px;height:16px;flex:none;color:#A79A8C}
  .glyph{width:18px;flex:none;text-align:center;font-size:14px;font-weight:800;color:#B3A596;line-height:1}
  .pill .arw{width:14px;height:14px;flex:none;color:#C9BEB2}
  footer{margin:24px 0 0;padding-top:16px;border-top:1px solid var(--line)}
  footer p{font-size:11px;line-height:1.7;color:#9C9083;margin:0}
  footer p + p{margin-top:7px}
  .copy{margin-top:12px!important;font-size:10px;color:#C2B7AB;letter-spacing:.01em}
  @media (min-width:520px){
    body{padding-top:56px}
    h1{font-size:29px}
  }
""".strip("\n")


def build() -> str:
    products = DATA.get("products", [])
    cards = "\n\n".join(card(p, i) for i, p in enumerate(products))
    links = "\n".join(link_pill(x) for x in DATA.get("links", []))
    brand = E(DATA.get("brand", "큐픽"))
    brand_en = E(DATA.get("brand_en", "Q.PICK"))
    tagline = E(DATA.get("tagline", ""))
    lines = DATA.get("tagline_lines") or [DATA.get("tagline", "")]
    h1_html = "<br>".join(
        E(line).replace("꿀템", '<span class="hl">꿀템</span>') for line in lines
    )
    intro = E(DATA.get("intro", ""))
    disclosure = E(DATA.get("disclosure", ""))
    notice = E(DATA.get("notice", ""))
    favicon = (
        "data:image/svg+xml,"
        "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
        "%3Crect width='64' height='64' rx='15' fill='%23DF5537'/%3E"
        "%3Cpath d='M32 16a16 16 0 1 0 11 27.6L49 49l-3.4-5.4' fill='none' stroke='%23fff' "
        "stroke-width='6' stroke-linecap='round'/%3E%3C/svg%3E"
    )
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{brand} · {brand_en} | 살림·자취 꿀템 링크모음</title>
<meta name="description" content="{tagline} {intro}">
<meta name="theme-color" content="#FBF7F1">
<meta name="color-scheme" content="light">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{brand} · {brand_en}">
<meta property="og:title" content="{brand} · {brand_en} | 살림·자취 꿀템 링크모음">
<meta property="og:description" content="{tagline}">
<meta property="og:url" content="https://0123wtq.github.io/qpick-links/">
<meta name="twitter:card" content="summary">
<link rel="icon" href="{favicon}">
<style>
{CSS}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <p class="brand"><b>{brand}</b><span class="dot">·</span><span class="en">{brand_en}</span></p>
    <h1>{h1_html}</h1>
    <p class="intro">{intro}</p>
  </header>
  <main>
{cards}
  </main>
  <nav class="links" aria-label="큐픽 채널 바로가기">
{links}
  </nav>
  <footer>
    <p>{disclosure}</p>
    <p>{notice}</p>
    <p class="copy">© {brand} {brand_en}</p>
  </footer>
</div>
</body>
</html>
"""


if __name__ == "__main__":
    out = ROOT / "index.html"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes, {len(DATA.get('products', []))} products)")
