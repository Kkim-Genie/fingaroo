# Fingaroo - 금융 정보 검색 및 분석 플랫폼

Fingaroo는 금융 정보를 검색하고 분석하는 AI 기반 플랫폼입니다. FastAPI 기반의 백엔드 API와 Next.js 기반의 웹 프론트엔드로 구성되어 있습니다.

## 🏗️ 프로젝트 구조

```
fingaroo/
├── api/                    # FastAPI 백엔드 서버
│   ├── app/               # 애플리케이션 코드
│   │   ├── agent/         # LangGraph 기반 AI 에이전트
│   │   ├── chat/          # 채팅 관련 기능
│   │   ├── dart/          # DART API 연동 기능
│   │   ├── crawl/         # 웹 크롤링 기능
│   │   └── utils/         # 유틸리티 함수들
│   ├── main.py           # 서버 진입점
│   ├── pyproject.toml    # Python 의존성 관리
│   ├── Dockerfile        # Docker 이미지 설정
│   └── docker-compose.yml # Docker Compose 설정
└── web/                   # Next.js 프론트엔드
    ├── app/              # Next.js 14 App Router
    ├── package.json      # Node.js 의존성 관리
    └── next.config.mjs   # Next.js 설정
```

## 🚀 실행 방법

### 1. 백엔드 API 서버 실행

#### 로컬 환경에서 실행

1. **fastapi 의존성 설정**

   ```bash
   cd api
   uv sync
   playwright install --with-deps
   ```

2. **fastapi 실행**

   ```bash
   cd api
   uv run main.py
   ```

   서버가 `http://localhost:8000`에서 실행됩니다.

### 2. 웹 프론트엔드 실행

#### 로컬 환경에서 실행

1. **Node.js 의존성 설치**

   ```bash
   cd web
   npm install
   ```

2. **개발 서버 실행**
   ```bash
   npm run dev
   ```
   웹 애플리케이션이 `http://localhost:3000`에서 실행됩니다.

#### 프로덕션 빌드

```bash
cd web
npm run build
npm start
```

## 📋 API 스펙

### 주요 엔드포인트

- `GET /` - 서버 상태 확인
- `GET /healthcheck` - 데이터베이스 연결 상태 확인
- `/chat/*` - 채팅 관련 API
- `/dart/*` - DART API 연동 기능

### 기술 스택

#### 백엔드 (API)

- **Framework**: FastAPI
- **Python**: 3.12+
- **AI/ML**:
  - LangChain
  - LangGraph
  - OpenAI API
  - Google Gemini API
- **데이터베이스**: PostgreSQL (SQLAlchemy)
- **웹 크롤링**: Playwright, Crawl4AI
- **의존성 관리**: uv

#### 프론트엔드 (Web)

- **Framework**: Next.js 14
- **언어**: TypeScript
- **스타일링**: Tailwind CSS
- **패키지 관리**: npm

## 🔧 주요 기능

### 1. AI 에이전트 시스템

- **LangGraph** 기반 멀티 에이전트 아키텍처
- **DART 에이전트**: 기업 재무정보 분석
- **검색 에이전트**: 네이버 뉴스 검색
- **주식 가격 에이전트**: 실시간 주식 정보 조회

### 2. DART API 연동

- 기업 재무제표 조회
- 기업 이벤트 정보 (배당, 자본변동 등)
- 다중 기업 재무지표 비교 분석

### 3. 웹 크롤링

- 네이버 뉴스 검색
- 금융 정보 수집
- 실시간 데이터 업데이트

## 📝 개발 가이드

### API 개발

1. `api/app/` 디렉토리에서 새로운 기능 추가
2. FastAPI 라우터를 사용하여 엔드포인트 정의
3. 의존성 주입을 통한 서비스 관리
4. experiment.ipynb에서 간단한 내용 테스트 (커널을 올바르게 인식하기 위해서는 api폴더에서 code/cursor를 열어야 함)
   ```bash
   cd api
   cursor .
   ```

### 웹 개발

1. `web/app/` 디렉토리에서 Next.js App Router 사용
2. TypeScript로 타입 안전성 보장
3. Tailwind CSS로 스타일링
