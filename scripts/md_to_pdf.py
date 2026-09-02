#!/usr/bin/env python3
"""프로젝트 내 모든 .md 파일을 PDF로 변환 (markdown -> html -> chrome headless print-to-pdf)."""
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "pdf"
CHROME = "/usr/bin/google-chrome-stable"

HTML_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  @page {{ size: A4; margin: 18mm 16mm; }}
  body {{
    font-family: "Noto Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", sans-serif;
    line-height: 1.65;
    color: #1a1a1a;
    font-size: 13px;
    word-break: keep-all;
  }}
  h1 {{ font-size: 22px; border-bottom: 2px solid #333; padding-bottom: 6px; margin-top: 0; }}
  h2 {{ font-size: 17px; border-bottom: 1px solid #ccc; padding-bottom: 4px; margin-top: 28px; color: #1f3a5f; }}
  h3 {{ font-size: 14.5px; margin-top: 20px; color: #2a4d7a; }}
  h4 {{ font-size: 13.5px; margin-top: 14px; }}
  code {{ background: #f2f2f2; padding: 1px 4px; border-radius: 3px; font-size: 12px; }}
  pre {{ background: #f5f5f5; padding: 10px; border-radius: 6px; overflow-x: auto; }}
  blockquote {{ border-left: 3px solid #999; margin: 8px 0; padding: 4px 14px; color: #444; background: #fafafa; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 12px; }}
  th, td {{ border: 1px solid #ccc; padding: 6px 8px; text-align: left; }}
  th {{ background: #eef2f7; }}
  hr {{ border: none; border-top: 1px dashed #bbb; margin: 24px 0; }}
  li {{ margin: 3px 0; }}
  a {{ color: #1a5fb4; }}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def md_to_pdf(md_path: Path, pdf_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    body_html = markdown.markdown(text, extensions=["extra", "sane_lists", "toc"])
    html = HTML_TEMPLATE.format(title=md_path.stem, body=body_html)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    html_tmp = pdf_path.with_suffix(".tmp.html")
    html_tmp.write_text(html, encoding="utf-8")
    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",
        f"file://{html_tmp}",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    html_tmp.unlink(missing_ok=True)
    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"PDF 생성 실패: {md_path.name}\n{result.stderr}")
    print(f"{md_path.relative_to(ROOT)} -> {pdf_path.relative_to(ROOT)} ({pdf_path.stat().st_size:,} bytes)")


def main() -> None:
    md_files = sorted(ROOT.glob("notes/*.md")) + sorted(ROOT.glob("markdown/*.md"))
    if not md_files:
        sys.exit("md 파일을 찾지 못했습니다.")
    for md_path in md_files:
        rel_dir = md_path.parent.name  # notes | markdown
        pdf_path = OUT_DIR / rel_dir / (md_path.stem + ".pdf")
        md_to_pdf(md_path, pdf_path)


if __name__ == "__main__":
    main()
