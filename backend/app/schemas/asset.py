from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AssetBase(BaseModel):
    project_id: str
    file_name: str
    metadata_json: Optional[Dict[str, Any]] = None

class AssetCreate(AssetBase):
    storage_uri: str

class AssetResponse(AssetBase):
    id: str
    storage_uri: str
    created_at: datetime

    class Config:
        from_attributes = True

class AssetUploadResponse(BaseModel):
    id: str
    storage_uri: str
    file_name: str
    project_id: str
