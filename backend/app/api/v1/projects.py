from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.services.project_service import ProjectService
from app.dependencies import get_project_service

router = APIRouter()

@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    service: ProjectService = Depends(get_project_service)
):
    return await service.create_project(project_in)

@router.get("", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0, limit: int = 100,
    service: ProjectService = Depends(get_project_service)
):
    return await service.list_projects(skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
):
    project = await service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project_in: ProjectUpdate,
    service: ProjectService = Depends(get_project_service)
):
    project = await service.update_project(project_id, project_in)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service)
):
    project = await service.delete_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
