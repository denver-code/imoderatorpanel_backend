from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    Request,
    Header
)
import json
from rauth import OAuth2Service
import app.api.config_api as cp
from functools import wraps
from fastapi_limiter.depends import RateLimiter

auth = APIRouter(prefix="/auth")

discord = OAuth2Service(
    name=cp.get_value("name"),
    client_id=cp.get_value("client_id"),
    client_secret=cp.get_value("client_secret"),
    access_token_url=cp.get_value("access_token_url"),
    authorize_url=cp.get_value("authorize_url"),
    base_url=cp.get_value("base_url")
)

authorize_url = discord.get_authorize_url(
        scope=cp.get_value("scope"),
        response_type= "code",
        redirect_uri=cp.get_value('redirect_uri')
)

async def login_required(Authorization = Header("Authorization")):
    try:
        session = discord.get_session(Authorization.split()[1])
        user = session.get('users/@me').json()
        if "message" in user:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")


@auth.post('/login', dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def login():
    return {"auth_url":authorize_url}


@auth.post('/discord', dependencies=[Depends(RateLimiter(times=1, seconds=5))])
async def discord_callback(code: str):
    try:
        key = {"key":"token", "value":discord.get_access_token(
            data={
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': cp.get_value("redirect_uri")
            },
            decoder=json.loads
        )}
        session = discord.get_session(key["value"])
        user = session.get('users/@me').json()
        if user["id"] in cp.get_value("white_list"):
            return key
        else:
            return HTTPException(status_code=400, detail="")
    except:
        raise HTTPException(status_code=404, detail="Token not found")
