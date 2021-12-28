import uvicorn
import app.api.config_api as cp

if __name__ == "__main__":
    uvicorn.run(
            "app.server:app",
            host="localhost",
            port=8393,
            debug=True,
            reload=True
            )
