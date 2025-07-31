# Fingaroo 뉴스 스크래퍼

Fingaroo 금융 플랫폼을 위한 한국 금융뉴스 수집용 웹 스크래퍼입니다. NestJS 기반으로 제작되었으며, Apify 액터로 실행되고 Puppeteer를 사용해 안정적인 웹 스크래핑을 제공합니다.

## 지원하는 뉴스 소스

### 1. 미래에셋증권

- **타입**: `miraeasset`
- **콘텐츠**: "AI 데일리 글로벌 마켓 브리핑" 일일 리포트
- **수집 방식**: Puppeteer 기반 네비게이션 및 콘텐츠 추출
- **URL 패턴**: securities.miraeasset.com의 날짜별 검색

### 2. 네이트 뉴스

- **타입**: `nate`
- **콘텐츠**: 경제 섹션 뉴스 기사
- **수집 방식**: EUC-KR 인코딩 처리를 통한 HTTP 요청
- **URL 패턴**: 일일 경제 뉴스 페이지

## 설치

```bash
# 의존성 설치
npm install
```

## 환경설정

필수 환경변수를 설정하세요:

```bash
# 뉴스 데이터를 전송할 API 엔드포인트
export AI_ADMIN_URL="https://your-api-endpoint.com" #fastapi url
```

## 사용법

### 로컬 개발

```bash
# 개발 모드 (변경사항 감지)
npm run start:dev

# 프로덕션 모드
npm run start:prod

# 프로젝트 빌드
npm run build
```

### 특정 스크래퍼 실행

스크래퍼는 입력값을 받아 수집할 뉴스 소스를 결정합니다:

```bash
# 미래에셋 뉴스 수집
brew install apify-cli
apify run --input '{"newsType":"miraeasset"}'

# 네이트 뉴스 수집
apify run --input '{"newsType":"nate"}'
```

### 사용 가능한 뉴스 타입

- `miraeasset`: 미래에셋증권 일일 브리핑
- `nate`: 네이트 경제 뉴스 기사

## 개발

### 프로젝트 구조

```
src/
├── app.module.ts          # 메인 NestJS 모듈
├── main.ts                # 진입점 및 Apify 액터 설정
├── scraper/               # 스크래퍼 구현체
│   ├── miraeasset.scraper.ts
│   └── nate.scraper.ts
└── util/
    ├── enum/
    │   └── news.enum.ts   # 뉴스 타입 정의
    ├── manager/
    │   └── news.manager.ts # 핵심 스크래핑 로직
    └── type/
        └── news.type.ts   # TypeScript 타입 정의
```

## 라이선스

UNLICENSED - Fingaroo 플랫폼 전용 프로젝트
