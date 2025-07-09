from fastapi import FastAPI, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.chat.interface.controllers.chat_controller import router as chat_routers
from app.dart.interface.controllers.dart_controller import router as dart_routers
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import get_db
from app.containers import Container

app = FastAPI()
container = Container()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 특정 도메인만 허용하도록 변경
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_routers)
app.include_router(dart_routers)

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