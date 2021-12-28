# from fastapi import (
#     APIRouter,
#     Depends,
#     Response,
#     Request,
#     Header,
#     HTTPException
# )
# import json
# import os
# import signal
# from starlette.responses import FileResponse
# from app.routes.auth import login_required
# from rauth import OAuth2Service
# import app.api.config_api as cp
# import subprocess
# import app.api.teleapi as telebot
# import time
# from fastapi_limiter.depends import RateLimiter

# discord = OAuth2Service(
#     name=cp.get_value("name"),
#     client_id=cp.get_value("client_id"),
#     client_secret=cp.get_value("client_secret"),
#     access_token_url=cp.get_value("access_token_url"),
#     authorize_url=cp.get_value("authorize_url"),
#     base_url=cp.get_value("base_url")
# )


# projects = APIRouter(prefix="/tech/projects")

# @projects.post("/toggle", dependencies=[Depends(login_required), Depends(RateLimiter(times=1, seconds=5))])
# async def toggle_app(id_name, Authorization = Header("Authorization")):
#     try:
#         cp.get_value("version",filep=f"app_data/{id_name}")
#     except:
#         raise HTTPException(status_code=404, detail="App not found!")
#     if cp.get_value("status",filep=f"app_data/{id_name}") == "OFF":
#         s = time.perf_counter()
#         try:
#             cp.set_value(name='status', value='ON',filep=f"app_data/{id_name}")
#             path = "\\".join(cp.get_value("execute_path",filep=f"app_data/{id_name}").split("\\")[:-1])
#             f = subprocess.Popen(f'cd {path} & python {cp.get_value("execute_path",filep=f"app_data/{id_name}")}', shell=True)
#             cp.set_value(name='process', value=str(f.pid) ,filep=f"app_data/{id_name}")
#             elapsed = time.perf_counter() - s
#             session = discord.get_session(Authorization.split()[1])
#             user = session.get('users/@me').json()
#             telebot.send_message(f"""✅iTechPanel:\nDeploy:{id_name} succeeded after {elapsed:0.2f}s!\nExecuted by:{user["id"]} {user["username"]}:{user["discriminator"]}\nEmail:{user["email"]}""")
#         except:
#             elapsed = time.perf_counter() - s
#             telebot.send_message(f"""❌iTechPanel:\nDeploy {id_name} failed after {elapsed:0.2f}s!\nExecuted by:{user["id"]} {user["username"]}:{user["discriminator"]}\nEmail:{user["email"]}""")
#     else:
#         s = time.perf_counter()
#         session = discord.get_session(Authorization.split()[1])
#         user = session.get('users/@me').json()
#         try:
#             subprocess.call(['taskkill', '/F', '/T', '/PID',  cp.get_value("process",filep=f"app_data/{id_name}")])
#             cp.set_value(name='status', value='OFF',filep=f"app_data/{id_name}")
#             elapsed = time.perf_counter() - s
#             telebot.send_message(f"""✅iTechPanel:\nKill task:{cp.get_value("process",filep=f"app_data/{id_name}")} name:{id_name} succeeded after {elapsed:0.2f}s!\nStatus - OFF❌\nExecuted by:{user["id"]} {user["username"]}:{user["discriminator"]}\nEmail:{user["email"]}""")
#         except:
#             elapsed = time.perf_counter() - s
#             telebot.send_message(f"""❌iTechPanel:\nKill task:{cp.get_value("process",filep=f"app_data/{id_name}")} name:{id_name} failed after {elapsed:0.2f}s!\nStatus - OFF❌\nExecuted by:{user["id"]} {user["username"]}:{user["discriminator"]}\nEmail:{user["email"]}""")
#     return {"message":"success"}, 200

# @projects.post('/list', dependencies=[Depends(login_required), Depends(RateLimiter(times=3, seconds=5))])
# async def project_list():
#     project_list = []
#     app_names = cp.get_array("apps")
#     for i in app_names:
#         if i:
#             app_info = {
#                 "id_name":cp.get_value("id_name", filep=f"app_data/{i}"),
#                 "name":cp.get_value("name", filep=f"app_data/{i}"),
#                 "status":cp.get_value("status", filep=f"app_data/{i}"),
#                 "mini_pick":cp.get_value("mini_pick", filep=f"app_data/{i}"),
#                 "feed":cp.get_value("feed", filep=f"app_data/{i}"),
#             }
#             project_list.append(app_info)
#     return {"apps":project_list}

# @projects.post('/app', dependencies=[Depends(login_required), Depends(RateLimiter(times=3, seconds=5))])
# async def project(id_name: str):
#     try:
#         app_names = cp.get_array("apps") 
#         if id_name in app_names:
#             app_info = {
#                 "id":cp.get_value("id", filep=f"app_data/{id_name}"),
#                 "id_name":cp.get_value("id_name", filep=f"app_data/{id_name}"),
#                 "version":cp.get_value("version", filep=f"app_data/{id_name}"),
#                 "name":cp.get_value("name", filep=f"app_data/{id_name}"),
#                 "status":cp.get_value("status", filep=f"app_data/{id_name}"),
#                 "description":cp.get_value("description", filep=f"app_data/{id_name}"),
#                 "banner":cp.get_value("banner", filep=f"app_data/{id_name}"),
#                 "mini_pick":cp.get_value("mini_pick", filep=f"app_data/{id_name}"),
#                 "command":cp.get_value("command", filep=f"app_data/{id_name}"),
#                 "tech":cp.get_value("tech", filep=f"app_data/{id_name}"),
#                 "feed":cp.get_value("feed", filep=f"app_data/{id_name}")
#             }
#             return app_info
#         else:
#                 raise HTTPException(status_code=404, detail="App not found!")
#     except:
#         raise HTTPException(status_code=404, detail="App not found!")

# @projects.get("/image", dependencies=[Depends(RateLimiter(times=5, seconds=5))])
# async def get_image(file_name: str):
#     try:
#         return FileResponse(file_name)
#     except:
#         raise HTTPException(status_code=404, detail="File not found!")
