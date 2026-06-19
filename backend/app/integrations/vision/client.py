import logging
import base64
from typing import Dict, Any, Optional
from app.core.config import settings
import asyncio
import json
from io import BytesIO

logger = logging.getLogger(__name__)

class VisionClient:
    """Client for connecting to IBM Vision AI or using IBM Granite for image analysis."""
    
    def __init__(self):
        self.api_key = settings.WATSONX_API_KEY
        self.project_id = settings.WATSONX_PROJECT_ID
        self.url = settings.WATSONX_URL
        
    def _extract_image_features(self, image_bytes: bytes, filename: str = "") -> str:
        """
        Extract basic visual features from image using PIL/Pillow.
        Returns a text description that can be analyzed by Granite.
        """
        try:
            from PIL import Image
            import numpy as np
            
            img = Image.open(BytesIO(image_bytes))
            
            # Get basic properties
            width, height = img.size
            mode = img.mode
            format_name = img.format or "Unknown"
            
            # Convert to RGB if needed for analysis
            if mode != 'RGB':
                img = img.convert('RGB')
            
            # Get dominant colors
            img_small = img.resize((50, 50))
            pixels = np.array(img_small)
            avg_color = pixels.mean(axis=(0, 1))
            
            # Determine color palette
            r, g, b = avg_color
            if r > 150 and g > 150 and b > 150:
                color_desc = "light/bright tones"
            elif r < 100 and g < 100 and b < 100:
                color_desc = "dark/shadowed tones"
            elif r > g and r > b:
                color_desc = "warm reddish tones"
            elif b > r and b > g:
                color_desc = "cool bluish tones"
            else:
                color_desc = "balanced neutral tones"
            
            # Aspect ratio analysis
            aspect = width / height
            if aspect > 1.3:
                orientation = "horizontal/landscape"
            elif aspect < 0.7:
                orientation = "vertical/portrait"
            else:
                orientation = "square/balanced"
            
            # Brightness analysis
            brightness = pixels.mean()
            if brightness > 180:
                lighting = "very bright, high-key lighting"
            elif brightness > 120:
                lighting = "well-lit, moderate brightness"
            elif brightness > 60:
                lighting = "subdued, low-key lighting"
            else:
                lighting = "very dark, dramatic shadows"
            
            # Contrast analysis
            std_dev = pixels.std()
            if std_dev > 70:
                contrast = "high contrast with strong shadows and highlights"
            elif std_dev > 40:
                contrast = "moderate contrast"
            else:
                contrast = "low contrast, soft gradations"
            
            description = f"""Image Analysis Report:
Filename: {filename}
Dimensions: {width}x{height} pixels
Format: {format_name}
Orientation: {orientation}
Color Palette: {color_desc}
Lighting: {lighting}
Contrast: {contrast}
Average RGB: ({int(r)}, {int(g)}, {int(b)})

This appears to be a sculpture or artwork photograph with the above visual characteristics."""
            
            return description
            
        except Exception as e:
            logger.warning(f"Failed to extract image features: {e}")
            return f"Image file: {filename}, unable to extract detailed features."
        
    async def analyze_image(self, image_bytes: bytes, mime_type: str = "image/jpeg", filename: str = "") -> str:
        """
        Stage 1: Image Captioning / Vision Model.
        Returns a rich text description of the uploaded image.
        If VISION_PROVIDER is mock, returns a realistic caption mock.
        """
        try:
            if settings.VISION_PROVIDER == "mock":
                await asyncio.sleep(1.0)
                # If the filename contains 'madonna', 'buddha', etc., we could return different captions.
                # For the hackathon demo, we will default to the Nataraja caption if generic.
                filename_lower = filename.lower()
                if "buddha" in filename_lower:
                    return "A stone sculpture depicting an enlightened deity seated in meditation. Triangular stability in posture, with a serene expression, a cranial bump (ushnisha), and monastic robe folds. The figure sits upon a stylized lotus throne."
                elif "ganesha" in filename_lower:
                    return "A voluminous stone carving of an elephant-headed deity. The figure has a large belly, one broken tusk, and holds a noose, goad, and a sweet. It is seated on a small mouse mount."
                elif "madonna" in filename_lower:
                    return "A marble sculpture of a mother and child. Features an S-curve posture, centralized focus, and intricate drapery folds characteristic of Renaissance art."
                else:
                    return "Bronze sculpture depicting a dancing Hindu deity with multiple arms. Circular aureole behind the figure. One foot placed upon a dwarf-like figure. Holding a drum and flame. Dynamic pose suggesting movement."
            else:
                # Actual Vision API Call (Mocked here as PIL extraction since tier is restricted)
                # In the future, this would call a real multimodal model (e.g. LLaVA or IBM Vision)
                image_description = await asyncio.to_thread(
                    self._extract_image_features,
                    image_bytes,
                    filename
                )
                return image_description
                
        except Exception as e:
            logger.error(f"Vision Image Captioning failed: {e}")
            raise

