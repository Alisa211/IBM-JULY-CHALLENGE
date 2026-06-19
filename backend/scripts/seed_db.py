import asyncio
import uuid
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import AsyncSessionLocal
from app.models.knowledge_chunk import SculptureKBEntry, AncientArtChunk

async def seed_sculpture_kb(db: AsyncSession):
    # Dummy data
    entries = [
        {
            "id": "kb-sculpt-001",
            "title": "David",
            "period": "Renaissance",
            "region": "Italy",
            "material": "Marble",
            "iconography": ["Heroic nude", "Sling", "Contrapposto"],
            "summary": "Michelangelo's David is a masterpiece of Renaissance sculpture.",
            "source": "Art History DB"
        },
        {
            "id": "kb-sculpt-002",
            "title": "Venus de Milo",
            "period": "Hellenistic",
            "region": "Greece",
            "material": "Marble",
            "iconography": ["Semi-nude", "Missing arms", "Draped lower body"],
            "summary": "An ancient Greek statue and one of the most famous works of ancient Greek sculpture.",
            "source": "Louvre Collection"
        }
    ]
    
    for entry_data in entries:
        existing = await db.execute(select(SculptureKBEntry).where(SculptureKBEntry.id == entry_data["id"]))
        if not existing.scalars().first():
            entry = SculptureKBEntry(**entry_data)
            # Create a dummy 384-dim zero vector
            entry.embedding = [0.0] * 384
            db.add(entry)
            
    await db.commit()
    print("Sculpture KB seeded successfully.")

async def seed_ancient_kb(db: AsyncSession):
    chunks = [
        {
            "id": "kb-ancient-001",
            "source": "Shilpa Shastra Vol 1",
            "text": "The ideal proportions of the human body are defined in terms of the tala system, where one tala is the distance from the hairline to the chin."
        },
        {
            "id": "kb-ancient-002",
            "source": "Vitruvian Proportions",
            "text": "The length of the outspread arms is equal to the height of a man, forming a perfect square."
        }
    ]
    
    for chunk_data in chunks:
        existing = await db.execute(select(AncientArtChunk).where(AncientArtChunk.id == chunk_data["id"]))
        if not existing.scalars().first():
            chunk = AncientArtChunk(**chunk_data)
            chunk.embedding = [0.0] * 384
            db.add(chunk)
            
    await db.commit()
    print("Ancient Art KB seeded successfully.")

async def main():
    async with AsyncSessionLocal() as db:
        await seed_sculpture_kb(db)
        await seed_ancient_kb(db)

if __name__ == "__main__":
    asyncio.run(main())
