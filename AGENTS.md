# AGENTS.md

이 파일은 이 저장소에서 작업하는 AI 코딩 에이전트를 위한 프로젝트 컨텍스트입니다.

## 프로젝트 개요

`실무자 AI 교육 1` 멀티캠퍼스 교육 과정(챕터 1~6, 248페이지)의 교안 PDF와 부록 자료를 학습하기 위한 개인 학습 프로젝트입니다. 코드를 작성/배포하는 프로젝트가 아니라 **문서 정리·요약·학습 진행 관리**가 목적입니다.

절대 경로: `/home/bjpark/projects/ai-education-study`
원본 자료 위치(Windows): `C:\Users\qazws\Desktop\교육\실무자AI교육1` (`/mnt/c/Users/qazws/Desktop/교육/실무자AI교육1`)

## 디렉터리 구조

```
source/         원본 자료 사본 (PDF 6종 원본 위치 참조, zip 압축 해제본, docx/html 부록)
  chapter_pdfs/    "Chapter1~6 전체 교안 PDF.zip" 해제본 — 파일명 인코딩 깨짐 있음(원본 PDF와 동일 내용, 사용 안 함)
  workflow_samples/ 챕터5 실습 산출물 예시 (docx/html/pdf)
markdown/        교안 PDF → 텍스트 추출 결과 (scripts/extract_pdfs.py 산출물)
notes/           챕터별/부록별 핵심 요약 노트 + 실행 가이드 (사람이 학습하는 핵심 자료)
pdf/             notes/, markdown/ 전체를 PDF로 변환한 결과 (scripts/md_to_pdf.py 산출물)
scripts/         PDF↔MD↔PDF 변환 스크립트
```

## 핵심 규칙

1. **credentials 파일은 git에 올리지 않는다.** `source/Gemini_인증용_계정안내.html`은 교육 참석자 계정/비밀번호가 평문으로 담긴 파일이라 `.gitignore`에 등록되어 있음. 유사한 민감 정보 파일이 추가되면 반드시 `.gitignore`에 먼저 추가할 것.
2. **PDF 텍스트 추출은 일반 text 모드로 하지 않는다.** 이 교안 PDF들은 슬라이드 형태라 PyMuPDF `get_text("text")`로 추출하면 단어가 한 글자~한 단어 단위로 줄바꿈되어 가독성이 심각하게 나빠진다. 반드시 `scripts/extract_pdfs.py`의 **blocks+clip 하이브리드 방식**을 사용할 것 (block 영역을 clip으로 재추출하고, 원문과 문자 수·구성이 다르면 원문 폴백 — 전체 페이지 문자 유실/중복 0 검증됨). 새 PDF를 추가로 추출할 때도 이 스크립트를 재사용/확장한다.
3. **다이어그램·스크린샷 등 이미지 전용 정보는 텍스트 추출로 잡히지 않는다.** 핵심 슬라이드(수치 다이어그램, UI 캡처, 취소선/색상 강조 등)는 `pymupdf`로 페이지를 PNG 렌더링한 뒤 vision 분석으로 확인하고, 노트에 `[이미지 확인]` 태그를 붙여 보강한다.
4. **실제 서비스 로그인이 필요한 실습(Gemini 등)은 에이전트가 대신 수행하지 않는다.** 사용자 계정으로 브라우저 로그인해 대리 수행하는 것은 사용자가 명시적으로 승인한 경우에만 진행하며, 기본값은 `notes/실행가이드_*.md` 형태의 체크리스트 문서를 만들어 사용자가 직접 수행하게 한다.
5. **노트 갱신 시 학습 계획도 함께 갱신한다.** `notes/00_학습계획.md`가 전체 진행 상황의 단일 소스(source of truth)이므로, 새 노트/실행가이드를 추가하거나 완료 표시할 때 체크리스트를 함께 갱신한다.
6. **모든 변경은 git 커밋으로 남긴다.** 이 저장소는 로컬 git 저장소이며(원격 없음), 의미 있는 작업 단위마다 한글 커밋 메시지로 기록한다.

## 스크립트

- `scripts/extract_pdfs.py` — 원본 PDF(`source/` 상위의 실제 위치, 위 절대경로 참고) → `markdown/*.md` 재추출. 원본 PDF가 갱신되면 재실행.
- `scripts/md_to_pdf.py` — `notes/*.md` + `markdown/*.md` → `pdf/notes/*.pdf` + `pdf/markdown/*.pdf` 일괄 변환 (markdown 파이썬 패키지 + Chrome headless print-to-pdf 사용). 노트 수정 후 PDF를 갱신하려면 재실행.
  - 의존성: `pip install markdown` (프로젝트 venv 없음, 시스템/활성 venv에 설치), `google-chrome-stable` 바이너리 필요.

## 학습 흐름 (사람 대상, 참고용)

`notes/00b_학습방법_가이드.md`에 상세 기술됨. 요약: README → 학습계획 → 챕터 1~6 노트(순서대로) → 부록 노트(선택) → 실행 가이드로 실습(브라우저 직접 수행) → 학습계획 체크.

## 하지 말 것

- `source/chapter_pdfs/`의 깨진 파일명 PDF를 참조하지 말 것 (원본 PDF와 100% 동일 내용, `source/` 상위 실제 원본 경로 사용).
- notes 파일을 대량 재작성하지 말 것 — 기존 노트는 `patch`로 섹션 단위 보강, 신규 주제만 새 파일 생성.
