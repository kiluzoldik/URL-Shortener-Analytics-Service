import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from app.api.dependencies import redis_lifespan
from app.api.shortener import short_router
from app.api.auth import auth_router
from app.api.redirect import redirect_router
    

app = FastAPI(title="URL Shortener", lifespan=redis_lifespan)

app.include_router(short_router)
app.include_router(auth_router)
app.include_router(redirect_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", reload=True, lifespan="on")