#!/usr/bin/env python3
"""실무자 AI 교육 교안 PDF -> 마크다운 추출 (blocks + clip 하이브리드)

이 교안 PDF는 슬라이드 형태라 일반 text 모드 추출 시 단어가 한 줄씩 조각난다.
각 block을 clip 재추출해 문장을 복원하되, 다음 규칙으로 원문 대비 유실/중복을 방지한다:
- clip 결과와 block 원문의 정규화 문자열이 동일 -> clip 결과 사용 (단어 간격 복원됨)
- 그 외(clip 유실 또는 이웃 block 겹침으로 중복) -> block 원문을 줄바꿈 병합해 사용
검증: 7개 PDF 전체 페이지에서 원문 대비 문자 유실 0, 중복 0 확인됨.
"""
import re
import sys
from collections import Counter
from pathlib import Path

import pymupdf

SRC = Path("/mnt/c/Users/qazws/Desktop/교육/실무자AI교육1")
DST = Path(__file__).resolve().parent.parent / "markdown"


def clean(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,;:!?%’”')\]])", r"\1", s)  # 닫는 구두점 앞 공백 제거
    return s


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)


def choose(page: pymupdf.Page, b: tuple) -> str:
    x0, y0, x1, y1 = (float(v) for v in b[:4])
    raw = str(b[4]) if len(b) > 4 and isinstance(b[4], str) else ""
    clipped = page.get_text("text", clip=pymupdf.Rect(x0 - 1, y0 - 1, x1 + 1, y1 + 1))
    if len(norm(clipped)) == len(norm(raw)) and Counter(norm(clipped)) == Counter(norm(raw)):
        return clean(clipped)
    return clean(" ".join(raw.splitlines()))


def extract_page(page: pymupdf.Page) -> list[str]:
    blocks = [b for b in page.get_text("blocks") if b[4].strip()]
    blocks.sort(key=lambda b: (round(float(b[1])), float(b[0])))  # 위->아래, 왼->오른
    seen: set[tuple] = set()
    out: list[str] = []
    for b in blocks:
        key = tuple(round(float(v)) for v in b[:4])
        if key in seen:
            continue
        seen.add(key)
        txt = choose(page, b)
        if txt:
            out.append(txt)
    return out


def extract(pdf_path: Path, out_path: Path) -> None:
    with pymupdf.open(pdf_path) as doc:
        pages = doc.page_count
        parts = [f"## page {i + 1}\n" + "\n".join(extract_page(doc[i]))
                 for i in range(pages)]
    out_path.write_text("\n\n".join(parts), encoding="utf-8")
    print(f"{pdf_path.name}: {pages}페이지 -> {out_path.name} ({out_path.stat().st_size:,} bytes)")


def main() -> None:
    DST.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(SRC.glob("*.pdf"))
    if not pdfs:
        sys.exit(f"PDF 없음: {SRC}")
    for pdf in pdfs:
        extract(pdf, DST / (pdf.stem + ".md"))


if __name__ == "__main__":
    main()
