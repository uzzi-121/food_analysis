# 🍳 CookCast AI (쿡캐스트 AI)
> **"보는 요리에서 듣는 요리로 — 냉장고 사진 한 장으로 완성되는 나만의 핸즈프리 오디오 셰프"**

CookCast AI는 [REFRIGERATOR_RECIPE_AI_AGENT_PLAN.md](REFRIGERATOR_RECIPE_AI_AGENT_PLAN.md) 기획안을 바탕으로 구현된 **최신 Python AI 에이전틱 클린 아키텍처(FastAPI + Pydantic v2 + 5-Agent 멀티 에이전트 파이프라인)** 및 **Stitch BETA 스타일의 AI-Native 다크 사이버네틱 UI/UX** 기반 음식 레시피 추천 및 핸즈프리 오디오 가이드 서비스입니다.

---

## 🌟 주요 특징 및 최신 아키텍처

### 1. 2025~2026 최신 Python 패키징 & 도메인 주도 클린 아키텍처
- **표준 `src/` 레이아웃 & PEP 621 `pyproject.toml`**:
  - 패키지 격리(Import Isolation), 빌드/배포 최적화, `pip install -e .` 및 Hatch/Poetry/uv 완벽 호환.
- **도메인 주도 에이전틱 클린 아키텍처 (Clean / Hexagonal)**:
  - `core/`: Pydantic-Settings v2 기반 타입 세이프 환경설정, 도메인 예외 계층, 구조화된 컬러 로거.
  - `domain/`: 순수 Python 모델(`models/`) 및 `typing.Protocol` 기반 인터페이스 규격(`protocols/`).
  - `agents/`: BaseAgent 추상 클래스를 상속받고 프로토콜을 준수하는 5대 독립 멀티 에이전트.
  - `workflows/`: 5-Agent 체이닝 및 오케스트레이션 파이프라인.
  - `infrastructure/adapters/`: Gemini 2.0 Flash, YouTube 셰프 지식, 웹 레시피 DB, Edge-TTS 신경망 음성 엔진 격리.
  - `api/`: FastAPI 앱 팩토리(`create_app`), 의존성 주입(DI), v1 라우터.
  - `cli.py`: 터미널에서 즉시 5-Agent 파이프라인을 테스트/시연할 수 있는 대화형 CLI 도구.

### 2. 5-Agent Multi-Agent Pipeline
- **Agent 1. Ingredient Vision Extractor (`vision_agent.py`)**: 냉장고 사진 또는 자연어 텍스트 기반 식재료 자동 감지, 분류 및 정규화
- **Agent 2. Recipe Harvester (`harvester_agent.py`)**: 백종원, 류수영 등 스타 셰프 꿀팁 및 인기 요리 지식 실시간 교차 탐색
- **Agent 3. Golden Recipe Synthesizer (`synthesizer_agent.py`)**: 최적의 양념 황금비율 도출, 냉장고 맞춤형 스마트 대체재 추천
- **Agent 4. Voice Script & SSML Crafter (`script_agent.py`)**: 친절한 라디오 셰프 감성 대본 및 조리 호흡 동기화 SSML 작성
- **Agent 5. TTS Audio Engine (`tts_agent.py`)**: 단계별(Step-by-step) 고품질 한국어 신경망 음원(MP3) 분할 렌더링 및 캐싱

### 3. Stitch BETA 감성의 AI-Native 사이버네틱 UI/UX (v1.1.0 New)
- **도트 매트릭스 그리드 (Dot Matrix Grid)**: 캔버스 전체에 펼쳐지는 미래지향적 매트릭스 패턴 배경.
- **네온 오로라 글로우 웨이브 (Aurora Glow Waves)**: 바이올렛(`#8B5CF6`), 사이버 블루(`#38BDF8`), 마젠타 핑크(`#EC4899`)의 다층 블러 유동 애니메이션.
- **미니멀 헤더 & 볼드 히어로**: `CookCast` 로고타입 + 캡슐형 `BETA` 배지 + `Neural Voice Ready` 상태등 + `Try now` 필 버튼.
- **중앙 플로팅 올인원 AI 프롬프트 카드 (Floating AI Prompt Card)**:
  - 넉넉한 텍스트 입력창, 첨부된 냉장고 사진 썸네일 칩, 네온 보라빛 캡슐형 식재료 태그 칩 집약.
  - 하단 툴바: `+` 사진 추가 버튼, `📸 사진 인식 / ✍️ 텍스트` 모드 캡슐, `✨ 황금비율 ⌵` 드롭다운, 마이크 음성 제어, `↑` 원형 화이트 실행 버튼.
- **네온 림 테크 카드**: 호버 시 네온 오로라 림 라인이 켜지는 인터랙티브 레시피 큐레이션 카드.
- **사이버네틱 오디오 셰프 모드**: 팟캐스트 스타일의 시크한 핸즈프리 플레이어, 실시간 파형(Waveform) 비주얼라이저, 디지털 카운트다운 타이머 & 음성 명령 지원.

---

## 📁 디렉토리 구조 (Modern Project Layout)

```
food_analysis/
├── pyproject.toml                  # PEP 621 표준 패키징, 의존성 & CLI 스크립트 정의
├── requirements.txt                # pip 호환 의존성 명세서
├── log.md                          # 📝 개발 이슈 및 해결 사항 누적 추적 기록 문서
├── README.md                       # 프로젝트 종합 안내서
├── run.py                          # 웹 애플리케이션 원클릭 실행 스크립트
├── .env.example                    # 환경변수 템플릿
├── .gitignore                      # 최적화된 파이썬/캐시/빌드 제외 설정
├── src/                            # 표준 src-layout
│   └── food_analysis/              # 메인 패키지
│       ├── __init__.py             # 패키지 버전 및 메타데이터
│       ├── cli.py                  # 터미널 대화형 인터랙티브 CLI
│       ├── core/                   # 코어 인프라 (config, exceptions, logger)
│       ├── domain/                 # 순수 도메인 계층
│       │   ├── models/             # Pydantic v2 DTO & 엔티티 (ingredient, recipe, audio)
│       │   └── protocols/          # Python Protocol 인터페이스 (agent, adapter)
│       ├── agents/                 # 5대 멀티 에이전트 모듈 (base, vision, harvester, synthesizer, script, tts)
│       ├── workflows/              # 워크플로우 & 오케스트레이션 (orchestrator.py)
│       ├── infrastructure/         # 외부 시스템 어댑터 (gemini, search, youtube, tts)
│       ├── api/                    # FastAPI 웹 API 계층 (app.py, dependencies.py, v1/)
│       ├── web/                    # 프론트엔드 UI 리소스
│       │   ├── templates/index.html   # Stitch 스타일 모던 웹 UI
│       │   └── static/             # 사이버네틱 CSS & 바닐라 JS (style.css, app.js, audio_player.js, speech.js)
│       └── storage/                # 로컬 파일 저장소 (uploads, audio, cache)
└── tests/                          # 테스트 스위트
    ├── conftest.py                 # Pytest 공통 픽스처
    ├── unit/                       # 단위 테스트 (test_agents.py, test_protocols.py)
    └── integration/                # 통합 테스트 (test_api.py)
```

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1. 패키지 설치 (Editable Mode)
```bash
pip install -e .
# 또는 일반 설치: pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택 사항)
API 키 없이도 스마트 시뮬레이션 및 내장된 Neural TTS를 통해 즉시 100% 정상 작동합니다. Google Gemini 비전 기능을 사용하려면 `.env` 파일을 생성하세요:
```bash
copy .env.example .env
```
`.env` 파일에 발급받은 `GEMINI_API_KEY`를 입력합니다.

### 3. 인터랙티브 터미널 CLI 실행
콘솔에서 5대 멀티 에이전트 파이프라인의 추천 과정을 즉시 확인할 수 있습니다:
```bash
# 콘솔 CLI 실행
python -m food_analysis.cli --ingredients "스팸, 김치, 계란, 대파"

# 또는 패키지 등록 스크립트 실행
food-analysis --ingredients "스팸, 김치, 계란, 대파"
```

### 4. 웹 애플리케이션 실행
```bash
python run.py
```
서버가 시작되면 웹 브라우저에서 아래 주소로 접속합니다:
- **웹 서비스 UI:** [http://localhost:8000](http://localhost:8000)
- **FastAPI 대화형 문서 (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **헬스 체크:** [http://localhost:8000/health](http://localhost:8000/health)

---

## 🧪 테스트 실행 (Run Tests)

```bash
pytest
# 또는 상세 결과: pytest -v
```
- 도메인 프로토콜 준수 검증: `tests/unit/test_protocols.py`
- 5대 에이전트 개별 기능 검증: `tests/unit/test_agents.py`
- FastAPI REST 엔드포인트 통합 검증: `tests/integration/test_api.py`

---

## 📝 이슈 및 해결 기록 관리 (Issue Tracking)

프로젝트 개발 및 유지보수 과정에서 발생하는 모든 버그, 기술적 결정 사항, 트러블슈팅 및 해결 내역은 [log.md](log.md) 파일에 지속적으로 누적 기록됩니다:
- **[ISSUE-001]**: 하위 디렉토리 중복 생성 및 Git 저장소 루트 승격 정상화
- **[ISSUE-002]**: PEP 621 `pyproject.toml` 및 표준 `src/` 레이아웃, 도메인 클린 아키텍처 개편
- **[ISSUE-003]**: Windows 터미널(CP949) 환경 유니코드 이모지 출력 인코딩 오류 해결
- **[ISSUE-004]**: Stitch BETA 스타일 AI-Native 다크 사이버네틱 UI/UX 전면 개편 및 기능 무결성 유지

---

## 📜 버전 릴리즈 노트 (Release History)

- **v1.1.0 (2026-09-16)**:
  - Stitch BETA 감성의 다크 사이버네틱 & 오로라 글래스모피즘 UI/UX 전면 리뉴얼.
  - 도트 매트릭스 그리드 캔버스 및 다층 네온 오로라 애니메이션 구현.
  - 중앙 플로팅 올인원 AI 프롬프트 카드 도입 (사진/텍스트 통합 입력, 모드 토글, 툴바).
  - 프로젝트 전용 이슈 및 트러블슈팅 기록 문서 (`log.md`) 체계 도입.
- **v1.0.0 (2026-09-16)**:
  - 현대적 표준 `src/` 레이아웃 및 PEP 621 `pyproject.toml` 구축.
  - 도메인 주도 5-Agent 멀티 에이전트 클린 아키텍처 수립.
  - 인터랙티브 콘솔 CLI 도구(`food_analysis.cli`) 개발.
  - 10개 단위/통합/프로토콜 테스트 스위트 구축.
