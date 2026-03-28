# words — SPEC

## 개요
피터공 개인 에세이 블로그. Bilingual (한/영). 미니멀 타이포그래피 중심.

## URL
- `mice3nyc.github.io/words/`
- GitHub repo: `mice3nyc/words`

## 디자인
- 흰 바탕 (#fff), 검정 텍스트 (#111)
- 폰트: Paperlogy (전체 통일)
- 강조 컬러: 단일 accent (링크, 강조)
- 커버 이미지 없음. 글 중간 이미지는 가능
- 미니멀 최우선. 장식 요소 없음

## 페이지 구조

### 홈 (글 목록)
- "words" 타이틀
- 포스트 목록: 제목 + 날짜
- 클릭 → 글 본문

### 글 본문
- 제목, 부제, 날짜
- 한영 좌우 병렬 (데스크탑)
- 상하 배치 (모바일)
- 플립 버튼: 좌우 ↔ 상하 토글 (사용자 선택)
- 글 중간 이미지 지원
- 목록으로 돌아가기

### 관리 (향후)
- 순서 변경 (드래그 앤 드롭)
- 공개/비공개 토글

## 데이터 구조

### posts.json (메타데이터)
```json
{
  "posts": [
    {
      "id": "001",
      "title": "문구록:연필.",
      "subtitle": "文具論 01",
      "date": "2016-05-05",
      "visible": true,
      "order": 1
    }
  ]
}
```

### 개별 포스트 (posts/001.json)
```json
{
  "id": "001",
  "title": "문구록:연필.",
  "subtitle": "文具論 01. 연필에 대해 기록하다",
  "date": "2016-05-05",
  "content_kr": "마크다운 본문 (한국어)",
  "content_en": "마크다운 본문 (영어)",
  "images": ["url1", "url2"]
}
```

## 기술 스택
- 단일 index.html
- 바닐라 JS (프레임워크 없음)
- CSS Grid/Flexbox
- marked.js (마크다운 렌더링, CDN)
- 반응형 (모바일 breakpoint: 768px)

## 포스팅 워크플로우
1. 피터공: 옵시디언에서 글 완성
2. 피터공: "올려줘"
3. 아리공: 마크다운 → JSON 변환 + 번역(필요시) + commit + push
4. GitHub Pages 자동 반영

## 콘텐츠 소스
- `_dev/brunch_backup/` 31편 (brunch_01~33, 결번 03·08·14)
- 전부 브런치에서 publish 상태였던 글
