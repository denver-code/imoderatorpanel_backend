from fastapi import (
    APIRouter,
    Depends,
    Header,
    Response
)
import json
from rauth import OAuth2Service
import app.api.config_api as cp
from app.routes.auth import login_required
from fastapi_limiter.depends import RateLimiter

user = APIRouter(prefix="/user")

discord = OAuth2Service(
    name=cp.get_value("name"),
    client_id=cp.get_value("client_id"),
    client_secret=cp.get_value("client_secret"),
    access_token_url=cp.get_value("access_token_url"),
    authorize_url=cp.get_value("authorize_url"),
    base_url=cp.get_value("base_url")
)

@user.post('/profile', dependencies=[Depends(login_required), Depends(RateLimiter(times=2, seconds=5))])
async def get_profile(Authorization = Header("Authorization")):
    session = discord.get_session(Authorization.split()[1])
    user_obj = session.get('users/@me').json()
    keys_to_remove = ["public_flags", "flags", "banner", "banner_color", "accent_color", "locale", "mfa_enabled"]
    for key in keys_to_remove:
        del user_obj[key]
    user_obj["avatar"] = await get_avatar(user_obj["id"], user_obj["avatar"])
    return user_obj


@user.post("/avatar", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def get_avatar(id: str, hash: str):
    return f"https://cdn.discordapp.com/avatars/{id}/{hash}.png"
