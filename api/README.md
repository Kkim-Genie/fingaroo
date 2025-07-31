# Fingaroo API 서버

Fingaroo는 AI 기반 투자 어시스턴트 시스템의 백엔드 API 서버입니다. 한국 주식시장 정보, DART API 연동, 투자 로그 관리 등의 기능을 제공합니다.

## 주요 기능

### 🤖 AI 어시스턴트

- 멀티 에이전트 시스템으로 구성된 대화형 AI
- 투자 관련 질문에 대한 지능적 응답
- 실시간 스트리밍 채팅 지원

### 📊 DART API 연동

- 한국 기업 재무정보 조회
- 재무제표, 배당 정보, 기업 이벤트 등
- 개별/연결 재무제표 구분 조회
- 기업 소송, 합병, 분할 정보

### 📈 주식 정보

- 실시간 주식 가격 조회
- 주식 차트 데이터 제공
- 종목별 상세 정보

### 📝 투자 로그 관리

- 매매일지 작성 및 관리
- 사용자 자산 현황 추적
- 투자 성과 분석
- AI 기반 투자 피드백

### 🔍 검색 및 정보

- 네이버 뉴스 검색
- 일일 시황 리포트
- 지식베이스 검색
- 금융 시세 정보

### 👤 사용자 관리

- JWT 기반 인증/인가
- 네이버 로그인 연동
- 사용자 프로필 관리

## 기술 스택

- **Framework**: FastAPI
- **AI/LLM**: LangChain, LangGraph, CLOVA Studio
- **Database**: PostgreSQL with pgvector
- **Authentication**: JWT, 네이버 OAuth
- **Dependencies**: UV (Python package manager)
- **Deployment**: Docker, Docker Compose

## 설치 및 실행

### 필수 요구사항

- Python 3.12+
- UV package manager
- PostgreSQL
- Docker (선택사항)

### 로컬 개발 환경

1. 의존성 설치:

```bash
uv sync
```

2. 환경변수 설정:
   `.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
LLM_MODEL_BASE=HCX-005
LLM_MODEL_HIGH=HCX-007
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret
DART_API_KEY=your_dart_api_key
CLOVASTUDIO_API_KEY=your_clova_api_key
SUPABASE_USER=your_db_user
SUPABASE_PASSWORD=your_db_password
SUPABASE_HOST=your_db_host
JWT_ACCESS_SECRET_KEY=your_jwt_secret
JWT_REFRESH_SECRET_KEY=your_refresh_secret
DATA_GO_API_KEY=your_data_go_key
```

3. 서버 실행:

```bash
uv run main.py
```

서버는 http://localhost:8000 에서 실행됩니다.

### Docker 실행

```bash
docker-compose up --build
```

## API 엔드포인트

### 헬스체크

- `GET /` - 서버 상태 확인
- `GET /healthcheck` - 데이터베이스 연결 상태 확인

### 채팅

- `POST /chat/first` - 새 대화 시작
- `POST /chat/continue` - 대화 이어가기
- `POST /chat/interrupt` - 대화 중단

### DART 정보

- `GET /dart/*` - 다양한 기업 정보 조회 엔드포인트

### 주식 정보

- `GET /stock-price/*` - 주식 가격 및 차트 정보

### 투자 로그

- `GET|POST|PUT|DELETE /invest-log/*` - 투자 로그 CRUD
- `GET|POST|PUT|DELETE /user-asset/*` - 사용자 자산 관리

### 뉴스 및 지식

- `GET /news/*` - 뉴스 검색 및 조회

### 사용자

- `POST /user/*` - 사용자 관리 및 인증

## 프로젝트 구조

```
api/
├── app/
│   ├── agent/              # AI 에이전트 시스템
│   │   ├── graphs/         # 에이전트 그래프 정의
│   │   ├── states/         # 상태 관리
│   │   └── tools/          # 에이전트 도구들
│   ├── chat/               # 채팅 기능
│   ├── dart/               # DART API 연동
│   ├── invest_log/         # 투자 로그 관리
│   ├── knowledge/          # 지식베이스 및 뉴스
│   ├── stock_price/        # 주식 가격 정보
│   ├── user/               # 사용자 관리
│   └── utils/              # 유틸리티 함수들
├── Dockerfile
├── docker-compose.yml
└── pyproject.toml
```

## 개발 환경

### 코드 스타일

- Python 코드는 Flake8으로 린팅
- 타입 힌트 사용 권장

### 데이터베이스

- PostgreSQL with pgvector extension
- SQLAlchemy ORM 사용
- 도메인 주도 설계(DDD) 패턴 적용

### 의존성 주입

- dependency-injector 패키지 사용
- 깔끔한 아키텍처 유지

## 라이센스

이 프로젝트는 개인/상업적 목적으로 사용 가능합니다.
