from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project_repo import project_repo
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.models.project import Project

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_project(self, project_in: ProjectCreate) -> Project:
        return await project_repo.create(self.db, obj_in=project_in)

    async def get_project(self, project_id: str) -> Optional[Project]:
        return await project_repo.get(self.db, id=project_id)

    async def list_projects(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return await project_repo.get_multi(self.db, skip=skip, limit=limit)

    async def update_project(self, project_id: str, project_in: ProjectUpdate) -> Optional[Project]:
        db_obj = await self.get_project(project_id)
        if not db_obj:
            return None
        return await project_repo.update(self.db, db_obj=db_obj, obj_in=project_in)

    async def delete_project(self, project_id: str) -> Optional[Project]:
        return await project_repo.delete(self.db, id=project_id)
