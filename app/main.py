from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.init_db import init_db 
from app.api import health, users, auth, protected, documents

# 서버가 시작될 때 실행할 로직 정의
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 켜질 때: DB 테이블 생성
    init_db()
    yield
    # 서버 꺼질 때: (필요하면 여기에 정리 코드 작성)

# lifespan을 FastAPI 앱에 등록
app = FastAPI(title="Docs Backend v0.1", lifespan=lifespan)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(protected.router)
app.include_router(documents.router)