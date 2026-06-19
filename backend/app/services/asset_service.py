import os
import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.asset_repo import asset_repo
from app.schemas.asset import AssetCreate
from app.models.asset import Asset
from app.core.config import settings

class MockStorageService:
    def __init__(self):
        # Create a local storage directory to mock cloud storage
        self.storage_dir = Path(settings.STORAGE_URL.replace('file://', ''))
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file: UploadFile) -> str:
        file_ext = os.path.splitext(file.filename)[1]
        unique_name = f"{uuid.uuid4()}{file_ext}"
        file_path = self.storage_dir / unique_name
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return f"file:///storage/{unique_name}"

    def generate_signed_url(self, storage_uri: str) -> str:
        """
        Mock implementation of Signed URL generation.
        In reality, this uses AWS S3 / IBM COS SDK to generate a pre-signed URL.
        """
        import time
        import hashlib
        expiration = int(time.time()) + 3600 # 1 hour
        sig = hashlib.md5(f"{storage_uri}{expiration}secret".encode()).hexdigest()
        return f"{storage_uri}?sig={sig}&exp={expiration}"

class AssetService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.storage = MockStorageService()

    async def upload_asset(self, project_id: str, file: UploadFile) -> Asset:
        # Upload to mock cloud storage
        storage_uri = await self.storage.upload_file(file)
        
        # Save metadata to database
        asset_in = AssetCreate(
            project_id=project_id,
            file_name=file.filename,
            storage_uri=storage_uri,
            metadata_json={"content_type": file.content_type, "size_bytes": file.size}
        )
        return await asset_repo.create(self.db, obj_in=asset_in)

    async def get_asset(self, asset_id: str) -> Optional[Asset]:
        asset = await asset_repo.get(self.db, id=asset_id)
        if asset:
            asset.storage_uri = self.storage.generate_signed_url(asset.storage_uri)
        return asset

    async def list_assets_by_project(self, project_id: str) -> List[Asset]:
        assets = await asset_repo.get_by_project(self.db, project_id=project_id)
        for asset in assets:
            asset.storage_uri = self.storage.generate_signed_url(asset.storage_uri)
        return assets
