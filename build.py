#!/usr/bin/env python3
"""
words — 빌드 스크립트 (마스터 → 배포 JSON)

소스(진실): _작가노트/_wordsposting/posts/*.md  (한영 마스터)
산출:        _dev/words/posts/{id}.json + posts.json (manifest) + images/ 동기화

워크플로우:
  옵시디언 _wordsposting/posts/ 에서 글 쓰기·수정
  → python3 build.py
  → git commit + push  → GitHub Pages 자동 반영

규칙:
- 글 파일명: NNN_제목.md (숨김글은 _NNN_제목.md, visible:false와 일치)
- 본문 구조: '## 한국어' ... '## English' ...
- frontmatter: title, title_en, subtitle, subtitle_en, date(ISO), visible, (brunch_num/keywords는 마스터 전용, JSON에 안 실림)
- manifest(posts.json) 순서 = 사이드바 순서. 기존 순서 보존, 새 글은 끝에 append(로그로 알림 → 수동 재배치).
- 이미지: 마스터 images/ → 배포 images/ 복사 (필터테스팅 테스트 이미지 제외)
"""
import json, glob, re, os, sys, shutil, unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
VAULT = os.path.abspath(os.path.join(ROOT, '..', '..'))
MD_DIR = os.path.join(VAULT, '_작가노트', '_wordsposting', 'posts')
MD_IMG = os.path.join(VAULT, '_작가노트', '_wordsposting', 'images')
JS_DIR = os.path.join(ROOT, 'posts')
JS_IMG = os.path.join(ROOT, 'images')
MANIFEST = os.path.join(ROOT, 'posts.json')

def clean(s):
    return unicodedata.normalize('NFC', (s or '').replace('\x08', ''))

def parse_md(path):
    raw = clean(open(path, encoding='utf-8').read())
    m = re.match(r'^---\n(.*?)\n---\n(.*)$', raw, re.S)
    if not m:
        raise ValueError(f'frontmatter 없음: {path}')
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'^(\w+):\s*(.*)$', line)
        if not mm:
            continue
        k, v = mm.group(1), mm.group(2).strip()
        if v[:1] in '"[':           # json 인용 스칼라/리스트
            try: v = json.loads(v)
            except Exception: pass
        fm[k] = v
    body = m.group(2)
    # 본문 분리: 첫 '## 한국어' ~ 첫 '## English'
    ik = body.find('## 한국어')
    ie = body.find('## English')
    if ik == -1 or ie == -1 or ie < ik:
        raise ValueError(f'한국어/English 헤딩 구조 이상: {path}')
    kr = body[ik + len('## 한국어'): ie].strip()
    en = body[ie + len('## English'):].strip()
    return fm, kr, en

def main():
    md_files = sorted(glob.glob(os.path.join(MD_DIR, '*.md')))
    if not md_files:
        sys.exit('마스터 글이 없습니다: ' + MD_DIR)
    records = {}
    for f in md_files:
        base = os.path.basename(f)
        mm = re.match(r'^_?(\d{3})_', base)
        if not mm:
            print(f'⚠ id 패턴 불일치, 건너뜀: {base}'); continue
        pid = mm.group(1)
        fm, kr, en = parse_md(f)
        vis = str(fm.get('visible', '')).lower() in ('true', '1', 'yes')
        rec = {
            'id': pid,
            'title': fm.get('title', ''),
            'title_en': fm.get('title_en', ''),
            'subtitle': fm.get('subtitle', ''),
            'date': str(fm.get('date', '')),
            'visible': vis,
            'content_kr': kr,
            'content_en': en,
            'subtitle_en': fm.get('subtitle_en', ''),
        }
        records[pid] = rec

    os.makedirs(JS_DIR, exist_ok=True)
    for pid, rec in records.items():
        with open(os.path.join(JS_DIR, f'{pid}.json'), 'w', encoding='utf-8') as fp:
            json.dump(rec, fp, ensure_ascii=False, indent=2)

    # manifest: 기존 순서 보존 + 새 글 append
    order = []
    if os.path.exists(MANIFEST):
        order = [e['id'] for e in json.load(open(MANIFEST, encoding='utf-8'))]
    new_ids = [p for p in records if p not in order]
    final = [p for p in order if p in records] + new_ids
    manifest = [{
        'id': r['id'], 'title': r['title'], 'title_en': r['title_en'],
        'subtitle': r['subtitle'], 'date': r['date'], 'visible': r['visible'],
    } for r in (records[p] for p in final)]
    with open(MANIFEST, 'w', encoding='utf-8') as fp:
        json.dump(manifest, fp, ensure_ascii=False, indent=2)

    # 이미지 동기화 (테스트 이미지 제외)
    copied = 0
    if os.path.isdir(MD_IMG):
        os.makedirs(JS_IMG, exist_ok=True)
        for name in os.listdir(MD_IMG):
            if name.startswith('.') or '필터테스팅' in name:
                continue
            src = os.path.join(MD_IMG, name)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(JS_IMG, name)); copied += 1

    print(f'✅ 빌드 완료: {len(records)}편 → posts/*.json')
    print(f'   manifest {len(manifest)}편 (순서 보존)' +
          (f', 새 글 append: {new_ids}  ← 사이드바 위치 재배치 필요' if new_ids else ''))
    print(f'   이미지 {copied}개 동기화')

if __name__ == '__main__':
    main()
