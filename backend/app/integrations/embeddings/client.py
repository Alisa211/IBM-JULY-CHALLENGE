from typing import List
import numpy as np

class EmbeddingsClient:
    """Client for generating vector embeddings from text."""
    
    def __init__(self):
        self.embedding_dimension = 384  # Standard for many lightweight models

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a vector embedding for the given text.
        For this sprint, it generates a deterministic mock vector based on string hash
        to allow pgvector pipelines to be tested without needing a live ML model.
        """
        # Mock logic: Create a normalized vector deterministically from the string hash
        import hashlib
        h = hashlib.md5(text.encode("utf-8")).digest()
        
        # We'll use the hash bytes to seed a random generator so it's deterministic
        seed = int.from_bytes(h[:4], "little")
        np.random.seed(seed)
        
        vec = np.random.randn(self.embedding_dimension)
        # Normalize
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
            
        return vec.tolist()

