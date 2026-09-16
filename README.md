# 🍳 CookCast AI (쿡캐스트 AI)
> **"보는 요리에서 듣는 요리로 — 냉장고 사진 한 장으로 완성되는 나만의 핸즈프리 오디오 셰프"**

CookCast AI는 [REFRIGERATOR_RECIPE_AI_AGENT_PLAN.md](REFRIGERATOR_RECIPE_AI_AGENT_PLAN.md) 기획안을 바탕으로 구현된 **최신 Python AI 에이전틱 클린 아키텍처(FastAPI + Pydantic v2 + 5-Agent 멀티 에이전트 파이프라인)** 기반 음식 레시피 추천 및 핸즈프리 오디오 가이드 서비스입니다.

---

## 🌟 주요 특징 및 최신 아키텍처

1. **2025~2026 최신 Python 패키징 및 클린 아키텍처:**
   - **표준 `src/` 레이아웃(PEP 621 `pyproject.toml`)**: 패키지 격리, `pip install -e .` 및 Hatch/Poetry/uv 완벽 호환.
   - **도메인 주도 에이전틱 클린 아키텍처 (Clean / Hexagonal)**:
     - `core/`: Pydantic-Settings v2 기반 타입 세이프 환경설정, 도메인 예외 계층, 구조화된 로거.
     - `domain/`: 프레임워크 무관 순수 Pydantic v2 도메인 모델(`models/`) 및 `typing.Protocol` 인터페이스 규격(`protocols/`).
     - `agents/`: BaseAgent 추상 클래스를 상속받고 프로토콜을 준수하는 5대 독립 멀티 에이전트.
     - `workflows/`: 5-Agent 체이닝 및 오케스트레이션 파이프라인.
     - `infrastructure/adapters/`: Gemini 2.0 Flash, YouTube 셰프 지식, 웹 레시피 DB, Edge-TTS 음성 엔진 격리.
     - `api/`: FastAPI 앱 팩토리, 의존성 주입(DI), v1 라우터.
     - `web/`: 반응형 글래스모피즘 웹 UI 및 정적 리소스.
     - `cli.py`: 터미널에서 즉시 5-Agent 파이프라인을 테스트/시연할 수 있는 대화형 CLI 도구.
2. **5-Agent Multi-Agent Pipeline:**
   - **Agent 1. Ingredient Vision Extractor:** 냉장고 사진 또는 자연어 텍스트 기반 식재료 자동 인식 및 정규화
   - **Agent 2. Recipe Harvester:** 백종원, 류수영 등 스타 셰프 팁 및 인기 레시피 지식 탐색
   - **Agent 3. Golden Recipe Synthesizer:** 양념 황금비율 도출, 냉장고 맞춤형 스마트 대체재 추천
   - **Agent 4. Voice Script & SSML Crafter:** 친절한 라디오 셰프 감성 대본 및 조리 호흡 동기화 SSML 작성
   - **Agent 5. TTS Audio Engine:** 단계별(Step-by-step) 고품질 한국어 신경망 음원(MP3) 분할 렌더링 및 캐싱
3. **핸즈프리 조리 모드 (Hands-free Chef Mode):**
   - 손에 물이나 양념이 묻어도 터치하기 쉬운 빅 컨트롤러 버튼
   - 단계별 자동 카운트다운 타이머 & 차임벨 알림 사운드
   - 오디오 파형(Waveform) 비주얼라이저 & 실시간 텔레프롬프터 대본 하이라이트
   - Web Speech API 기반 음성 제어 ("다음", "이전", "다시") 지원

---

## 📁 디렉토리 구조 (Modern Project Layout)

```
food_analysis/
├── pyproject.toml                  # PEP 621 표준 패키징, 의존성 & CLI 스크립트 정의
├── requirements.txt                # pip 호환 의존성 명세서
├── .env.example                    # 환경변수 템플릿
├── .gitignore                      # 최적화된 파이썬/캐시/빌드 제외 설정
├── README.md                       # 프로젝트 종합 안내서
├── run.py                          # 웹 애플리케이션 원클릭 실행 스크립트
├── src/                            # 표준 src-layout
│   └── food_analysis/              # 메인 패키지
│       ├── __init__.py             # 패키지 버전 및 메타데이터
│       ├── cli.py                  # 터미널 대화형 인터랙티브 CLI
│       ├── core/                   # 코어 인프라
│       │   ├── config.py           # Pydantic-Settings v2 환경설정
│       │   ├── exceptions.py       # 도메인 커스텀 예외 계층
│       │   └── logger.py           # 구조화된 컬러 로깅 설정
│       ├── domain/                 # 순수 도메인 계층
│       │   ├── models/             # Pydantic v2 DTO & 엔티티 (ingredient, recipe, audio)
│       │   └── protocols/          # Python Protocol 인터페이스 (agent, adapter)
│       ├── agents/                 # 5대 멀티 에이전트 모듈
│       │   ├── base.py             # BaseAgent 추상 클래스
│       │   ├── vision_agent.py     # Agent 1 (식재료 시각 인식 & 파싱)
│       │   ├── harvester_agent.py  # Agent 2 (셰프 레시피 탐색)
│       │   ├── synthesizer_agent.py# Agent 3 (황금 비율 종합 & 대체재)
│       │   ├── script_agent.py     # Agent 4 (라디오 셰프 SSML 대본화)
│       │   └── tts_agent.py        # Agent 5 (단계별 오디오 분할 렌더링)
│       ├── workflows/              # 워크플로우 & 오케스트레이션
│       │   └── orchestrator.py     # 5-Agent 파이프라인 총괄 제어기
│       ├── infrastructure/         # 외부 시스템 어댑터 (Ports & Adapters)
│       │   └── adapters/
│       │       ├── gemini_client.py   # Google GenAI (Gemini 2.0 Flash)
│       │       ├── search_client.py   # 레시피 데이터베이스 & 매칭 엔진
│       │       ├── youtube_client.py  # 셰프 채널 인사이트
│       │       └── tts_engine.py      # Edge-TTS / Cloud TTS 신경망 음성
│       ├── api/                    # FastAPI 웹 API 계층
│       │   ├── app.py              # FastAPI 앱 팩토리 & 수명주기 관리
│       │   ├── dependencies.py     # DI 컨테이너
│       │   └── v1/                 # API v1 라우터들 (ingredients, recipes, audio)
│       ├── web/                    # 웹 프론트엔드 리소스
│       │   ├── templates/index.html   # 모던 싱글페이지 웹 UI
│       │   └── static/             # 글래스모피즘 CSS & 바닐라 JS
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
API 키가 없어도 스마트 폴백과 내장된 Neural TTS를 통해 즉시 100% 정상 작동합니다. Google Gemini 비전 기능을 사용하려면 `.env` 파일을 생성하세요:
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

---

## 🧪 테스트 실행 (Run Tests)

```bash
pytest
# 또는 상세 결과: pytest -v
```
- 도메인 프로토콜 준수 검증: `tests/unit/test_protocols.py`
- 5대 에이전트 개별 기능 검증: `tests/unit/test_agents.py`
- FastAPI REST 엔드포인트 통합 검증: `tests/integration/test_api.py`
