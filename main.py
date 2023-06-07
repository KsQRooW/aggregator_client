from fastapi import FastAPI
import uvicorn

from routers.pages import pages_router
from routers.api import api_router


app = FastAPI()
app.include_router(pages_router)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0")
