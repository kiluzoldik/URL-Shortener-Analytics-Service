import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from app.api.short import short_router


app = FastAPI(title="URL Shortener")

app.include_router(short_router)


if __name__ == "__main__":
    uvicorn.run("app:main", host="0.0.0.0", reload=True)