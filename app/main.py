from fastapi import FastAPI
from app.api import health, users, auth, protected

app = FastAPI(title="Docs Backend v0.1")

app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(protected.router)