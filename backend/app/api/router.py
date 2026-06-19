from fastapi import APIRouter
from app.api.v1 import projects, assets, analysis, ideas, style, pipeline, telemetry, sculpture, health, outcomes

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(assets.router, prefix="/assets", tags=["assets"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])
api_router.include_router(style.router, prefix="/style", tags=["style"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["telemetry"])
api_router.include_router(sculpture.router, prefix="/sculpture", tags=["sculpture"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(outcomes.router, prefix="/outcomes", tags=["outcomes"])
