import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from app.api.dependencies import RedisDep
from app.api.shortener import short_router
from app.api.auth import auth_router
    

app = FastAPI(title="URL Shortener", lifespan=RedisDep)

app.include_router(short_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True)