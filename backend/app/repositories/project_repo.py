from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.repositories.base import BaseRepository

class ProjectRepository(BaseRepository[Project, ProjectCreate, ProjectUpdate]):
    pass

project_repo = ProjectRepository(Project)
