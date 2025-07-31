# Fingaroo - AI 기반 금융 정보 검색 및 투자 관리 플랫폼

Fingaroo는 AI와 대화하며 금융 정보를 검색하고 분석할 수 있는 지능형 플랫폼입니다. 사용자는 AI 채팅을 통해 기업 정보, 주식 데이터, 뉴스를 검색하고, 개인 투자 포트폴리오를 관리할 수 있습니다.

## 🏗️ 프로젝트 구조

```
fingaroo/
├── api/                    # FastAPI 백엔드 서버
│   ├── app/               # 애플리케이션 코드
│   │   ├── agent/         # LangGraph 기반 AI 에이전트
│   │   │   ├── graphs/    # 에이전트 워크플로우
│   │   │   ├── states/    # 에이전트 상태 관리
│   │   │   └── tools/     # DART, 검색 등 도구
│   │   ├── chat/          # AI 채팅 관련 기능
│   │   ├── dart/          # DART API 연동 (기업 재무정보)
│   │   ├── invest_log/    # 투자 일지 관리
│   │   ├── user/          # 사용자 관리
│   │   ├── stock_price/   # 주식 가격 정보
│   │   ├── knowledge/     # 뉴스 및 데이터 관리
│   │   └── utils/         # 유틸리티 함수들
│   ├── main.py           # 서버 진입점
│   ├── pyproject.toml    # Python 의존성 관리
│   ├── Dockerfile        # Docker 이미지 설정
│   └── docker-compose.yml # Docker Compose 설정
├── web/                   # Next.js 프론트엔드
│   ├── app/              # Next.js 14 App Router
│   │   ├── page.tsx      # 메인 채팅 페이지
│   │   ├── invest-log/   # 투자 관리 페이지
│   │   ├── layout.tsx    # 앱 레이아웃
│   │   └── types.ts      # TypeScript 타입 정의
│   ├── components/       # React 컴포넌트
│   │   ├── ChatContainer.tsx     # 채팅 인터페이스
│   │   ├── Messages.tsx          # 메시지 표시
│   │   ├── InvestLogModal.tsx    # 투자 일지 모달
│   │   ├── UserAssetModal.tsx    # 자산 관리 모달
│   │   └── StockChart.tsx        # 주식 차트
│   ├── business/         # 비즈니스 로직
│   │   ├── hooks/        # React 커스텀 훅
│   │   ├── services/     # API 서비스
│   │   └── utils/        # 유틸리티 함수
│   ├── store/           # Zustand 상태 관리
│   ├── package.json     # Node.js 의존성 관리
│   └── next.config.mjs  # Next.js 설정
└── scraper/             # Node.js 뉴스 스크래퍼
    └── src/             # 스크래핑 로직
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

3. **주요 기능**
   - **메인 페이지**: AI 채팅 인터페이스 (`/`)
   - **투자 관리**: 투자 일지 및 보유 자산 관리 (`/invest-log`)
   - **네이버 로그인**: 소셜 로그인 콜백 처리 (`/naverCallback`)

#### 프로덕션 빌드

```bash
cd web
npm run build
npm start
```

#### 개발 도구

```bash
# 린트 체크
npm run lint

# TypeScript 타입 체크
npx tsc --noEmit
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

- **Framework**: Next.js 14 (App Router)
- **언어**: TypeScript
- **스타일링**: Tailwind CSS
- **UI 라이브러리**: Mantine Core
- **상태 관리**: Zustand
- **HTTP 클라이언트**: Axios
- **차트**: ApexCharts
- **날짜 처리**: dayjs
- **마크다운**: React Markdown
- **패키지 관리**: npm

## 🔧 주요 기능

### 1. AI 채팅 인터페이스

- **자연어 대화**: AI와 자연스러운 대화를 통한 금융 정보 조회
- **실시간 스트리밍**: 답변을 실시간으로 받아볼 수 있는 스트리밍 UI
- **인터럽트 처리**: 대화 중 사용자 개입 및 방향 전환 가능
- **마크다운 지원**: 구조화된 답변 표시

### 2. 투자 포트폴리오 관리

- **투자 일지**: 매수/매도 기록 관리 및 손익 계산
- **보유 자산**: 현재 보유 중인 주식 및 자산 관리
- **투자 성과 분석**: 수익률 및 손익 통계 제공
- **데이터 시각화**: 투자 데이터를 표와 차트로 표시

### 3. AI 에이전트 시스템

- **LangGraph** 기반 멀티 에이전트 아키텍처
- **DART 에이전트**: 기업 재무정보 분석
- **검색 에이전트**: 네이버 뉴스 검색
- **주식 가격 에이전트**: 실시간 주식 정보 조회

### 4. DART API 연동

- 기업 재무제표 조회
- 기업 이벤트 정보 (배당, 자본변동 등)
- 다중 기업 재무지표 비교 분석

### 5. 웹 크롤링 및 데이터 수집

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

1. **페이지 개발**: `web/app/` 디렉토리에서 Next.js 14 App Router 사용

   - `page.tsx`: 메인 채팅 인터페이스
   - `invest-log/page.tsx`: 투자 관리 페이지
   - `layout.tsx`: 전체 앱 레이아웃

2. **컴포넌트 개발**: `web/components/` 디렉토리에서 재사용 가능한 컴포넌트 작성

   - `ChatContainer.tsx`: 채팅 메인 컨테이너
   - `Messages.tsx`: 메시지 표시 컴포넌트
   - Modal 컴포넌트들: 투자 일지, 자산 관리

3. **비즈니스 로직**: `web/business/` 디렉토리에서 관리

   - `hooks/`: React 커스텀 훅 (채팅, 투자 로그 등)
   - `services/`: API 통신 서비스
   - `utils/`: 유틸리티 함수

4. **상태 관리**: Zustand를 활용한 전역 상태 관리

   - `store/`: 각 도메인별 스토어 관리

5. **스타일링**: Tailwind CSS + Mantine 컴포넌트 라이브러리

6. **타입 안전성**: TypeScript로 엄격한 타입 체크
   - `app/types.ts`: 공통 타입 정의
