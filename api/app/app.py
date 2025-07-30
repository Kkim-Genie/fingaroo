
from fastapi import FastAPI, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.chat.interface.controllers.chat_controller import router as chat_routers
from app.dart.interface.controllers.dart_controller import router as dart_routers
from app.knowledge.interface.controllers.news_controller import router as news_routers
from app.user.interface.controller.user_controller import router as user_routers
from app.stock_price.interface.controller.stock_price_controller import router as stock_price_routers
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.containers import Container
from app.utils.langgraph import embedding_string

app = FastAPI()

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
app.include_router(user_routers)
app.include_router(stock_price_routers)

@app.get("/")
def server_check():
    return {"status": "ok"}

@app.get("/healthcheck")
async def health_check(db: Session = Depends(get_db)):
    try:
        # 데이터베이스에 간단한 쿼리를 실행하여 연결 확인
        # 현재 PostgreSQL 버전과 관계없이 안정적으로 작동합니다.
        result = db.execute(text("SELECT * FROM dart_corp_code limit 1;"))
        print(result.fetchall())
        return {"status": "ok", "database_connection": "successful"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")

@app.get("/embeddingCheck")
async def embedding_check():
    embeddig = await embedding_string("Hello, world!")
    return embeddig