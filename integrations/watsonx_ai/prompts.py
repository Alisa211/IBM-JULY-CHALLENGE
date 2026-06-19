"""
Watsonx.ai Prompt Templates

This module contains all prompt templates used for different AI tasks.
Each template is designed to produce structured, consistent outputs.
"""

IDEA_GENERATION_PROMPT = """You are an expert creative director specializing in sculpture and ancient art forms.

Task:
Generate exactly 3 unique sculpture concept ideas based on the provided brief.

Brief:
{brief}

Requirements:
- Each concept must be distinct and innovative
- Draw inspiration from ancient art traditions when relevant
- Consider materiality, form, and cultural context
- Provide actionable creative direction

Return your response as a JSON array with exactly 3 objects, each containing:
- title: A compelling, concise title (max 60 characters)
- description: Detailed concept description (150-300 words)
- artistic_rationale: Why this concept works artistically (100-200 words)
- materials: Suggested materials (comma-separated list)
- scale: Suggested scale/dimensions
- cultural_references: Relevant cultural or historical references

Format your response as valid JSON only, no additional text:
[
  {{
    "title": "...",
    "description": "...",
    "artistic_rationale": "...",
    "materials": "...",
    "scale": "...",
    "cultural_references": "..."
  }}
]
"""

CRITIQUE_PROMPT = """You are an expert art critic with deep knowledge of sculpture, ancient art, and contemporary practice.

Task:
Provide a detailed critique of the following sculpture concept.

Concept:
Title: {title}
Description: {description}

Analyze from these perspectives:
1. Artistic Merit: Originality, vision, conceptual strength
2. Technical Feasibility: Material considerations, structural integrity
3. Cultural Sensitivity: Appropriate use of cultural references
4. Market Potential: Appeal, uniqueness, collectibility

Return your response as a JSON object:
{{
  "overall_score": <1-10>,
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "suggestions": ["...", "..."],
  "artistic_merit": <1-10>,
  "technical_feasibility": <1-10>,
  "cultural_sensitivity": <1-10>,
  "market_potential": <1-10>,
  "detailed_analysis": "..."
}}
"""

STYLE_DNA_PROMPT = """You are an expert art historian and visual analyst.

Task:
Analyze the artistic style and characteristics of the provided artwork description.

Artwork Description:
{description}

Extract and identify:
1. Visual Style: Dominant aesthetic characteristics
2. Cultural Influences: Historical and geographical origins
3. Technical Approach: Methods and techniques evident
4. Emotional Tone: Mood and atmosphere
5. Key Motifs: Recurring patterns or symbols

Return your response as a JSON object:
{{
  "style_name": "...",
  "period": "...",
  "cultural_origin": "...",
  "characteristics": ["...", "..."],
  "color_palette": ["...", "..."],
  "techniques": ["...", "..."],
  "mood": "...",
  "similar_artists": ["...", "..."],
  "key_elements": ["...", "..."]
}}
"""

def format_prompt(template: str, **kwargs) -> str:
    """
    Format a prompt template with provided parameters.
    
    Args:
        template: The prompt template string
        **kwargs: Variables to inject into the template
        
    Returns:
        Formatted prompt string
    """
    return template.format(**kwargs)

# Made with Bob
