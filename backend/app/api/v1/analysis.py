from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.analysis import AnalysisRequest, JobResponse, AnalysisResponse
from app.services.analysis_service import AnalysisService
from app.services.cache_service import CacheService
from app.dependencies import get_analysis_service, get_cache_service

router = APIRouter()

@router.post("/run", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
async def run_analysis(
    request: AnalysisRequest,
    service: AnalysisService = Depends(get_analysis_service)
):
    job_id = await service.start_analysis_job(request.asset_id, request.analysis_type)
    return JobResponse(job_id=job_id, status="processing", message="Analysis job submitted")

@router.get("/job/{job_id}")
async def get_job_status(
    job_id: str,
    cache: CacheService = Depends(get_cache_service)
):
    status_data = await cache.get_job_status(job_id)
    if not status_data:
        raise HTTPException(status_code=404, detail="Job not found")
    return status_data

@router.get("/asset/{asset_id}", response_model=List[AnalysisResponse])
async def get_analysis_by_asset(
    asset_id: str,
    service: AnalysisService = Depends(get_analysis_service)
):
    return await service.get_analysis_by_asset(asset_id)
