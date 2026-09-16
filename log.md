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

---

## [2026-09-16] 릴리즈 1.2.0: 레시피 큐레이션 매칭 정밀도 고도화 및 멀티미디어 조리 가이드

### 📌 [ISSUE-005] '두부 조림' 질의 시 엉뚱한 레시피(스팸 김치볶음밥) 추천 오류 및 멀티미디어 조리 가이드 구축
- **상태**: ✅ 해결 완료 (Resolved)
- **발생 배경**:
  - 사용자가 보유 식재료 `[두부, 대파, 양파]`와 함께 "매콤한 두부 조림 알려줘"를 요청했으나, 1순위 추천으로 '스팸 김치볶음밥(96%)', 2순위 '차돌 된장찌개', 3순위 '돼지고기 김치찌개'가 노출되는 엉뚱한 결과 발생.
  - 사용자가 요청한 "단계별 절차에 따른 좌측 텍스트 / 우측 이미지 연동" 및 "하단 공인 셰프 유튜브 영상 플레이어 및 타임라인" 기능 반영 필요.
- **원인 분석**:
  1. **레시피 카탈로그 누락**: `search_client.py`의 데이터베이스에 `spicy-braised-tofu`(매콤 두부조림) 레시피가 등록되어 있지 않았음.
  2. **의도 분석 휴리스틱 키워드 미스매치**: `gemini_client.py`의 의도 분석 시뮬레이터에 '두부조림', '조림' 규칙이 없어 카탈로그 1번 기본값(`spam-kimchi-fried-rice`)으로 폴백되고, `harvester_agent.py`가 이를 1순위(96점)로 강제 승격시킴.
  3. **식재료 폴백 규칙 공백**: `has_tofu`가 있고 김치가 없는 경우(두부+대파+양파)에 대한 처리 규칙이 부재하여 엉뚱한 메뉴로 폴백됨.
- **해결 방안**:
  1. **고조회수 황금 레시피 등록 (AGENTS.md 대원칙 준수)**:
     - `search_client.py`: 백종원식 매콤 두부조림 (`spicy-braised-tofu`, 주재료: 두부/대파/양파) 추가.
     - `youtube_client.py`: 백종원 PAIK JONG WON 채널의 누적 조회수 **520만 회** 공식 영상(`w2X3P78C7n4`) 메타데이터 및 4대 챕터 타임라인 바인딩.
     - `synthesizer_agent.py`: 4단계 표준 조리 절차(재료 손질 ➡️ 양파 깔기 ➡️ 양념장 붓기 ➡️ 자작하게 조리기)와 단계별 이미지 URL 연결.
  2. **의도 분석 엔진 정밀도 고도화 (`gemini_client.py`)**:
     - 직접 요리명 매칭(Direct Dish Matching) 최우선 순위 신설: 사용자가 `두부조림`, `된장찌개`, `김치찌개`, `볶음밥`, `계란말이` 등을 직접 요청 시 1순위 즉시 바인딩.
     - 보유 재료 스마트 폴백: `has_tofu and not has_kimchi` 조건 시 `spicy-braised-tofu` 자동 추천.
  3. **단계별 조리 가이드 UI/UX 완성**:
     - 좌측 텍스트(조리 가이드, 셰프 꿀팁, 타이머, 불 조절), 우측 반응형 SVG 일러스트레이션 카드 렌더링.
     - 4개 전용 SVG 에셋(`spicy-braised-tofu_step1~4.svg`) 제작 완료.
     - 하단 유튜브 플레이어 및 챕터 원클릭 타임스탬프 이동 인터랙션 구현.
- **검증 결과**:
  - `curl /api/v1/recipes/discover` 호출 시 `spicy-braised-tofu`가 1순위(적합도 88%, 의도점수 96%)로 정확히 추천됨.
  - `tests/unit/test_agents.py` 및 `tests/integration/test_api.py` 13개 단위/통합 테스트 100% 통과 (0.03s).

---

## [2026-09-16] 릴리즈 1.3.0: 단일 집중형 순차 스텝 조리 뷰 및 실시간 텍스트 음성(TTS) 읽기 개편

### 📌 [ISSUE-006] 레시피 절차 뷰의 군더더기 섹션 제거, 단일 스텝 순차 노출 및 차례별 음성 읽기 구현
- **상태**: ✅ 해결 완료 (Resolved)
- **발생 배경**:
  - 기존 조리 화면에 오디오 스테이지, 사이드바 5종(재료, 양념 비율, 시크릿 팁 등), 수직 나열된 전체 단계 리스트, 하단 유튜브 플레이어가 한 화면에 복잡하게 렌더링되어 요리 중 시선이 분산됨.
  - 사용자의 "단계별 절차만 남기고 나머지는 다 지우고, 5개 절차가 있다면 한 번에 1개씩만 순차적으로 보여주며, 각 차례가 진행될 때 해당 텍스트를 음성으로 읽도록 해달라"는 명확한 요구사항 접수.
- **원인 분석**:
  - 이전 버전에서 정보 제공을 위해 사이드바 및 모든 단계 카드를 동시에 DOM에 노출시켰으나, 실제 요리 환경에서는 현재 해야 할 1개 작업에만 집중할 수 있는 미니멀 인터페이스가 필요함.
- **해결 방안**:
  1. **군더더기 섹션 전면 제거 (`index.html`)**:
     - 기존 사이드바 5종, 복합 오디오 스테이지, 하단 유튜브 플레이어 제거.
     - 요리명/소요시간 헤더 + 스텝 프로그레스 바 + 단일 스텝 집중 카드(`single-step-stage-card`)만으로 극단적 미니멀화.
  2. **1스텝 순차 디스플레이 구조화**:
     - 상단 Stepper 바(`STEP 01`, `STEP 02`...) 및 진행 퍼센트 바 연동.
     - 현재 활성화된 스텝 1개만 좌측 가이드/대본 + 우측 일러스트로 렌더링.
     - 하단에 [이전 단계], [다시 듣기], [음성 재생/일시정지], [다음 단계 (마지막 단계 시 '요리 완성!')] 컨트롤러 배치.
  3. **단계 진행 시 차례별 텍스트 실시간 TTS 자동 발화 (`audio_player.js`)**:
     - `selectStep(index, autoPlay=true)` 호출 시 현재 스텝의 대본(`audio_script`)을 음원 파일 또는 Web Speech API(`ko-KR`)로 즉각 재생.
     - 스텝 전환 시 음성 파형 애니메이션과 볼륨 아이콘 하이라이트 동기화.
     - 타이머가 있는 단계의 경우 음성 안내 종료 후 인라인 타이머 즉시 연동.
  4. **섹션 2(AI 추천 결과 그리드) 마크업 복구 및 안정화**:
     - 템플릿 마크업 교체 중 일시적으로 잘렸던 `#sectionRecipes` 및 `#recipeCardsContainer` 정상 복구.
     - 중복 ID(`playStatusText`) 제거 및 오디오 이벤트 리스너 null-guard 추가.
- **검증 결과**:
  - 브라우저 서빙 HTTP 200 정상 확인 및 단위/통합 테스트 13건 100% 통과.
  - '두부조림' 검색 시 AI 큐레이션 카드 정상 노출 및 단일 스텝 순차 전환 / 한국어 음성 낭독 완벽 동작.

