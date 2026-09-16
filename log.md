# 📝 CookCast AI — 이슈 및 해결 기록 (Issue & Resolution Log)

프로젝트 개발 과정에서 발생한 모든 이슈(Issue), 원인 분석(Root Cause), 해결 방안(Resolution) 및 검증 결과(Verification)를 체계적으로 기록하는 문서입니다.

---

## [2026-09-16] 릴리즈 1.1.0: Stitch BETA 스타일 UI/UX 전면 개편

### 📌 [ISSUE-004] Stitch 스타일 다크 사이버네틱 UI/UX 개편 및 DOM 기능 무결성 유지
- **상태**: ✅ 해결 완료 (Resolved)
- **발생 배경**:
  - 사용자가 요청한 "Stitch BETA" 사이트 감성의 최신 AI-Native 다크 인터페이스(도트 매트릭스 그리드, 네온 오로라 웨이브, 플로팅 올인원 프롬프트 카드)로 전면 리뉴얼 필요.
  - 마크업 구조 변경 시 기존의 5-Agent API 연동, 식재료 태그 관리, 파일 업로드, 그리고 핸즈프리 오디오 플레이어(`audio_player.js`)와 음성 인식(`speech.js`)의 DOM 이벤트 리스너가 끊길 위험성 존재.
- **원인 분석**:
  - `audio_player.js`와 `app.js`가 특정 ID(`audioElement`, `stepPillsContainer`, `currentStepTitle`, `dropzonePreview`, `playIcon` 등)에 강하게 결합되어 있어 단순 템플릿 교체 시 자바스크립트 런타임 오류 발생 가능.
- **해결 방안**:
  1. **Stitch 디자인 시스템 구축 (`style.css`)**:
     - 딥 옵시디언 다크 테마(`--bg-space: #07080E`) 적용.
     - 도트 매트릭스 그리드 패턴(`radial-gradient` + 타원형 마스크) 배경 렌더링.
     - 다층 네온 오로라 웨이브(`@keyframes aurora-drift`, `aurora-float`) 애니메이션 구현.
     - Stitch 시그니처 중앙 플로팅 AI 프롬프트 카드(`border-radius: 24px`, 다크 글래스모피즘, 림 라이트).
  2. **DOM ID 100% 보존 마크업 (`index.html`)**:
     - 플로팅 프롬프트 카드 내부에 `textIngredientInput`, `photoInput`, `dropzonePreview`, `ingredientTagContainer`, `btnFindRecipes`(`↑` 원형 버튼), `btnTriggerPhoto`(`+` 버튼) 완벽 배치.
     - 오디오 플레이어 엔진이 요구하는 `<audio id="audioElement">`, `#stepPillsContainer`, `#currentStepTitle`, `#currentSpokenScript`, `#playIcon` 등을 네온 테크 레이아웃에 일치화.
  3. **인터랙션 보강 (`app.js`)**:
     - 프롬프트 카드의 `+` 버튼 클릭 시 숨겨진 파일 선택창 연동.
     - Enter 키 누름 시 태그 추가 및 자동 실행 흐름 최적화.
- **검증 결과**:
  - `pytest tests/` 10개 테스트 100% 통과 (0.30s).
  - 로컬 웹 서버(`http://localhost:8000`) 접속 시 HTML 및 CSS 200 OK 응답 및 정상 렌더링 확인.

---

## [2026-09-16] 릴리즈 1.0.0: 최신 트렌드 폴더 구조 및 아키텍처 개편

### 📌 [ISSUE-003] Windows 콘솔(CP949) 환경에서 유니코드 이모지 출력 시 인코딩 오류
- **상태**: ✅ 해결 완료 (Resolved)
- **발생 배경**:
  - 터미널 인터랙티브 CLI(`python -m food_analysis.cli`) 실행 시 크래시 발생.
- **원인 분석**:
  - `cli.py`에서 출력한 이모지(🍳 `\U0001f373` 등)가 Windows 한글 콘솔 기본 코드페이지인 `CP949`에서 인코딩되지 않아 `UnicodeEncodeError: 'cp949' codec can't encode character...` 발생.
- **해결 방안**:
  - `cli.py` 및 `run.py` 상단에 Windows 환경 감지 시 `sys.stdout.reconfigure(encoding="utf-8")` 및 `sys.stderr.reconfigure(encoding="utf-8")`를 적용하여 터미널 표준 입출력을 UTF-8로 안전하게 재설정.
- **검증 결과**:
  - `python -m food_analysis.cli --ingredients "스팸, 김치, 계란, 대파"` 실행 시 크래시 없이 정상적으로 5대 에이전트 파이프라인 결과 출력 완료.

---

### 📌 [ISSUE-002] 패키징 표준(`src/` 레이아웃 & `pyproject.toml`) 부재 및 구조 레거시화
- **상태**: ✅ 해결 완료 (Resolved)
- **발생 배경**:
  - 기존 프로젝트가 단순 루트 `app/` 디렉토리 기반으로 구성되어 있어 패키지 격리(Import Isolation), 빌드/배포 최적화 및 `pip install -e .` 명령어 지원 불가.
- **원인 분석**:
  - 현대 파이썬(PEP 518/621) 표준 패키징 설정 파일인 `pyproject.toml`이 누락되었고, 레이어드 클린 아키텍처 간의 프로토콜 인터페이스(Interfaces) 규격이 정의되어 있지 않았음.
- **해결 방안**:
  1. PEP 621 표준 `pyproject.toml` 작성 및 CLI 진입점(`[project.scripts]`) 등록.
  2. `src/food_analysis/` 표준 `src/` 레이아웃 도입.
  3. **도메인 주도 에이전틱 클린 아키텍처**로 모듈 분리:
     - `core/`: 환경설정, 커스텀 예외, 구조화된 로거
     - `domain/`: Pydantic v2 모델(`models/`) 및 `typing.Protocol` 기반 규격(`protocols/`)
     - `agents/`: `BaseAgent` 기반 5대 독립 멀티 에이전트
     - `workflows/`: `orchestrator.py` 파이프라인 오케스트레이터
     - `infrastructure/adapters/`: 외부 API(Gemini, Search, YouTube, TTS) 어댑터
     - `api/`: FastAPI 앱 팩토리 및 의존성 주입(DI)
     - `web/`: 템플릿 및 정적 리소스
- **검증 결과**:
  - `pip install -e .` 성공적으로 빌드 및 설치 완료.
  - `tests/unit/test_protocols.py`를 통해 모든 에이전트의 Protocol 규격 준수 100% 검증.

---

### 📌 [ISSUE-001] 하위 디렉토리 중복 생성 및 Git 저장소 분리 문제
- **상태**: ✅ 해결 완료 (Resolved)
- **발생 배경**:
  - 프로젝트 루트에 `food_analysis/` 하위 폴더가 또 존재하고, `.git`이 하위 폴더에만 들어 있어 루트 디렉토리에서 Git 상태 추적 및 커밋/푸시가 불가능했던 현상.
- **원인 분석**:
  - 초기 설정 시 현재 폴더에서 `git clone https://github.com/uzzi-121/food_analysis.git`을 수행하면서 상위 폴더와 하위 폴더가 중복 생성됨.
- **해결 방안**:
  1. 하위 폴더의 `.git`을 프로젝트 루트 디렉토리(`food_analysis/`)로 안전하게 이동.
  2. 비어 있는 중복 하위 디렉토리 완전 제거.
  3. `.gitignore`를 최신 파이썬 및 앱 스토리지 캐시 제외 규칙에 맞춰 작성.
- **검증 결과**:
  - 프로젝트 루트에서 `git status` 실행 시 `On branch main`, 원격 저장소(`origin/main`)와 완벽히 동기화 확인.
