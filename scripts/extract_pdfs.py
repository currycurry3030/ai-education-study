#!/usr/bin/env python3
"""실무자 AI 교육 교안 PDF -> 마크다운 추출 스크립트"""
import sys
from pathlib import Path

import pymupdf

SRC = Path("/mnt/c/Users/qazws/Desktop/교육/실무자AI교육1")
DST = Path.home() / "projects/ai-education-study/markdown"


def extract(pdf_path: Path, out_path: Path) -> None:
    with pymupdf.open(pdf_path) as doc:
        parts = []
        for i in range(doc.page_count):
            text = doc[i].get_text("text").strip()
            parts.append(f"<!-- page {i + 1} -->\n{text}")
        pages = doc.page_count
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
