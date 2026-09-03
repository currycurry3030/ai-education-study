# 실무자 AI 교육 1 — 학습 프로젝트

`C:\Users\qazws\Desktop\교육\실무자AI교육1` 교안 자료를 체계적으로 학습하기 위한 프로젝트.

## 디렉터리 구조

- `source/` — 원본 자료 사본 (PDF 6개 교안은 원본 위치에서 직접 추출)
  - `workflow_samples/` — "AI활용Workflow_산출물_샘플.zip" 압축 해제본
- `markdown/` — 교안 PDF에서 추출한 전체 텍스트 (페이지 번호 주석 포함)
- `notes/` — 챕터별 학습 노트 (학습하며 작성)
- `scripts/` — PDF→마크다운 추출 스크립트

## 교안 목록 (248페이지)

| 챕터 | 제목 | 페이지 |
|------|------|--------|
| 1 | 과정 소개 및 환경 설정 | 53 |
| 2 | 최신 AI 트렌드와 Top 4 AI 툴 소개 | 71 |
| 3 | AI를 활용한 콘텐츠 생성 및 문서 제작 | 15 |
| 4 | 최신 AI 환경의 프롬프트 엔지니어링 | 39 |
| 5 | AI 활용 Workflow 실습 | 46 |
| 6 | Gems를 활용한 자산화 | 24 |

### 부록 자료

- `[Perplexity] 메모리_로봇 트렌드 보고서.pdf` (15p) → `markdown/` 추출 완료
- `[딥리서치 1] 메모리 및 로봇 기술 인사이트.docx`
- `[딥리서치 2] AI 스마트폰 런칭 기획안.docx`
- `프롬프트_CopyBook.html` — 프롬프트 복사북
- `Gemini_인증용_계정안내.html` — 교육용 제미나이 계정 안내 (**credentials 포함 — .gitignore로 git 추적 제외**)
- `workflow_samples/` — 챕터 5 실습 산출물 예시 (docx/html/pdf)

## 사용법

교안 재추출 (원본 PDF가 갱신된 경우):

```bash
python3 scripts/extract_pdfs.py
```

## 학습 방법

전체 학습 순서는 `notes/00b_학습방법_가이드.md` 참고. 요약하면:
1. `README.md` + `notes/00_학습계획.md`로 전체 그림 파악
2. `notes/1_...md` ~ `notes/6_...md` 순서대로 챕터 요약 학습
3. `notes/7~10_부록_*.md`로 심화 학습 (선택)
4. `notes/실행가이드_챕터5_workflow실습.md`, `notes/실행가이드_챕터6_미션7_Gem제작.md`로 실제 브라우저 실습
5. `notes/00_학습계획.md` 체크리스트 갱신
