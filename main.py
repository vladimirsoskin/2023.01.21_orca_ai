from fastapi import FastAPI

from events.cache_db import init_cache
from events.handlers import router as events_router

app = FastAPI()

app.include_router(events_router)


@app.on_event("startup")
def on_startup():
    init_cache()
