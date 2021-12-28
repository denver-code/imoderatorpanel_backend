import uvicorn
import app.api.config_api as cp

if __name__ == "__main__":
    uvicorn.run("app.server:app", host=cp.get_value("host"), port=int(cp.get_value("port")), debug=cp.get_bool("debug"), reload=True)