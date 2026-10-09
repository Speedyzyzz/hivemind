from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.sessions import router as sessions_router
from app.api.leases import router as leases_router
from app.api.interventions import router as interventions_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Collaborative Multiplayer Durable-Agent Runtime"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router, prefix=settings.API_V1_STR)
app.include_router(leases_router, prefix=settings.API_V1_STR)
app.include_router(interventions_router, prefix=settings.API_V1_STR)

@app.get("/healthz")
async def healthcheck():
    return {
        "status": "ok",
        "service": "hivemind-runtime",
        "version": settings.VERSION,
        "coordination": "event-sourced-fsm"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8003, reload=True)
