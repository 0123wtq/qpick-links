# 큐픽 · Q.PICK 링크모음

인스타 릴스 계정 **@q.pickqpick** 의 프로필 링크용 페이지입니다.
https://0123wtq.github.io/qpick-links/

## 매일 상품 추가하는 법

1. `products.json` 의 `products` 배열 **맨 위**에 새 상품을 추가합니다. `id`는 다음 번호(`02`, `03` …)로.
2. `python3 build.py` 실행 → `index.html` 이 다시 만들어집니다.
3. `git add -A && git commit -m "add #02 ..." && git push`

`index.html` 은 직접 고치지 마세요. 빌드하면 덮어써집니다. (내용·디자인 모두 `products.json` 과 `build.py` 안의 템플릿에서 나옵니다.)

## 상품 항목

```json
{
  "id": "02",
  "category": "주방",
  "name": "상품명",
  "option": "옵션 · 색상",          // 없으면 생략
  "hook": "한 줄 후킹 문구",
  "price": "8,900원",
  "original_price": "11,000원",     // 없으면 생략
  "discount": "19%",                // 없으면 생략
  "main": { "label": "쿠팡에서 보기", "url": "https://link.coupang.com/a/..." },
  "sub": [
    { "label": "네이버 클립 영상", "url": "https://naver.me/...", "icon": "play" }
  ]
}
```

- `main.url` 은 쿠팡 파트너스 단축링크, `sub` 는 클립·블로그 등 보조 링크(여러 개 가능, `icon` 은 `play` 또는 생략).
- 페이지 맨 아래 `links`(스레드·블로그·오픈채팅)와 `disclosure`(공정위 문구)도 `products.json` 에서 관리합니다.
- `tagline_lines` 로 상단 문구의 줄바꿈을 지정합니다.

## 파일

| 파일 | 설명 |
| --- | --- |
| `products.json` | 페이지 내용 전체(상품·바로가기 링크·공정위 문구) |
| `build.py` | `products.json` → `index.html` 생성기 |
| `index.html` | 결과 페이지(생성물, 외부 요청 0건 · 약 9KB) |
| `.nojekyll` | GitHub Pages Jekyll 처리 생략 |

## 고지

상품 링크는 쿠팡 파트너스 및 네이버 쇼핑 커넥트 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.
