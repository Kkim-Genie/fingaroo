from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.chat.interface.controllers.chat_controller import router as chat_routers
from app.dart.interface.controllers.dart_controller import router as dart_routers
from app.knowledge.interface.controllers.news_controller import router as news_routers
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.containers import Container
from google import genai
from google.genai.types import EmbedContentConfig
from app.config import get_settings
from app.knowledge.interface.schedulers.report_scheduler import init_scheduler, start_scheduler, shutdown_scheduler, get_jobs, test_scheduler_async

settings = get_settings()


# lifespan 컨텍스트 매니저 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI 애플리케이션의 시작 및 종료 이벤트를 관리합니다.
    """
    print("FastAPI: 애플리케이션 시작 이벤트 감지 (lifespan).")
    init_scheduler()  # 스케줄러 초기화 및 작업 추가
    start_scheduler() # 스케줄러 시작
    print("FastAPI: 스케줄러 설정 완료 (lifespan).")
    yield  # 애플리케이션이 실행되는 동안 대기
    print("FastAPI: 애플리케이션 종료 이벤트 감지 (lifespan).")
    shutdown_scheduler() # 스케줄러 종료
    print("FastAPI: 스케줄러 종료 완료 (lifespan).")

app = FastAPI(lifespan=lifespan)

# CORS 미들웨어를 가장 먼저 추가하여 preflight 요청을 우선 처리
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.fingaroo.vercel.app"],  # 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "Cache-Control",
        "X-Requested-With"
    ],
    expose_headers=["*"],
    max_age=3600,  # preflight 결과 캐시 시간
)

# Trusted Host 미들웨어 추가 (보안 강화) - CORS 다음에 배치
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

container = Container()

app.include_router(chat_routers)
app.include_router(dart_routers)
app.include_router(news_routers)

@app.get("/")
def server_check():
    return {"status": "ok"}

@app.get("/healthcheck")
async def health_check(db: Session = Depends(get_db)):
    try:
        # 데이터베이스에 간단한 쿼리를 실행하여 연결 확인
        # 현재 PostgreSQL 버전과 관계없이 안정적으로 작동합니다.
        result = db.execute(text("SELECT * FROM ai.dart_corp_code limit 1;"))
        print(result.fetchall())
        return {"status": "ok", "database_connection": "successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@app.get("/embeddingCheck")
async def embedding_check():
    client = genai.Client(vertexai=True, project=settings.GOOGLE_CLOUD_PROJECT, location=settings.GOOGLE_CLOUD_LOCATION)
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=["Hello, world!"],
        config=EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",  # Optional
        ),
    )
    return response

@app.get("/schedulers")
async def list_scheduled_jobs():
    """
    현재 스케줄러에 등록된 작업 목록을 반환합니다. (디버깅용)
    """
    jobs = get_jobs()
    job_details = []
    for job in jobs:
        job_details.append({
            "id": job.id,
            "name": job.name,
            "trigger": str(job.trigger),
            "next_run_time": job.next_run_time.isoformat() if job.next_run_time else "None"
        })
    return {"jobs": job_details}