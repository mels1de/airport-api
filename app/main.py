from fastapi import FastAPI,Depends
from app.config.config import settings,Settings
from app.api.routers.airport import router as airport_router
from app.api.routers.auth import router as auth_router

def get_settings():
    return settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(airport_router,prefix="/airports", tags=["airports"])

@app.get("/health")
async def healthcheck(config: Settings = Depends(get_settings)):
    return {"status": "ok", "app": config.app_name}
