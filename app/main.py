from fastapi import FastAPI,Depends
from app.config.config import settings,Settings

def get_settings():
    return settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

@app.get("/health")
async def healthcheck(config: Settings = Depends(get_settings)):
    return {"status": "ok", "app": config.app_name}
