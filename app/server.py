import aioredis
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth,
    user,
    projects,
    news
)
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter



app = FastAPI(title="iTechPanel")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://localhost")
    await FastAPILimiter.init(redis)


app.include_router(auth.auth, prefix="/api")
app.include_router(user.user, prefix="/api")
app.include_router(news.news, prefix="/api")
# app.include_router(projects.projects, prefix="/api")