from fastapi import (
    APIRouter,
    Depends,
    Header,
)
from app.routes.auth import login_required
import app.api.config_api as cp
from fastapi_limiter.depends import RateLimiter

news = APIRouter(prefix="/news")

@news.post("/posts", dependencies=[Depends(login_required), Depends(RateLimiter(times=1, seconds=5))])
async def posts_list(Authorization = Header("Authorization")):
    return {"message":"success"}, 200
