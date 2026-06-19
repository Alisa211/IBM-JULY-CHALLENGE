"""
Watsonx.ai Response Parser

This module converts raw LLM outputs into structured Python objects.
Handles JSON parsing, validation, and error recovery.
"""

import json
import re
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class ParserError(Exception):
    """Raised when parsing fails"""
    pass


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON content from text that may contain additional formatting.
    
    Args:
        text: Raw text that may contain JSON
        
    Returns:
        Extracted JSON string
    """
    # Try to find JSON array or object
    json_patterns = [
        r'\[[\s\S]*\]',  # JSON array
        r'\{[\s\S]*\}',  # JSON object
    ]
    
    for pattern in json_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return text


def parse_idea_cards(raw_response: str) -> List[Dict[str, Any]]:
    """
    Parse raw LLM response into structured idea cards.
    
    Args:
        raw_response: Raw text response from Watsonx
        
    Returns:
        List of idea card dictionaries
        
    Raises:
        ParserError: If parsing fails
    """
    try:
        # Extract JSON from response
        json_text = extract_json_from_text(raw_response)
        
        # Parse JSON
        ideas = json.loads(json_text)
        
        # Validate structure
        if not isinstance(ideas, list):
            raise ParserError("Response is not a JSON array")
        
        if len(ideas) == 0:
            raise ParserError("No ideas generated")
        
        # Validate each idea has required fields
        required_fields = ['title', 'description', 'artistic_rationale']
        validated_ideas = []
        
        for idx, idea in enumerate(ideas):
            if not isinstance(idea, dict):
                logger.warning(f"Idea {idx} is not a dictionary, skipping")
                continue
            
            # Check required fields
            missing_fields = [f for f in required_fields if f not in idea]
            if missing_fields:
                logger.warning(f"Idea {idx} missing fields: {missing_fields}, skipping")
                continue
            
            # Add defaults for optional fields
            idea.setdefault('materials', 'Not specified')
            idea.setdefault('scale', 'Not specified')
            idea.setdefault('cultural_references', 'Not specified')
            
            validated_ideas.append(idea)
        
        if not validated_ideas:
            raise ParserError("No valid ideas after validation")
        
        return validated_ideas
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        logger.error(f"Raw response: {raw_response[:500]}")
        raise ParserError(f"Failed to parse JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected parsing error: {e}")
        raise ParserError(f"Failed to parse response: {str(e)}")


def parse_critique(raw_response: str) -> Dict[str, Any]:
    """
    Parse raw LLM response into structured critique.
    
    Args:
        raw_response: Raw text response from Watsonx
        
    Returns:
        Critique dictionary
        
    Raises:
        ParserError: If parsing fails
    """
    try:
        json_text = extract_json_from_text(raw_response)
        critique = json.loads(json_text)
        
        if not isinstance(critique, dict):
            raise ParserError("Response is not a JSON object")
        
        # Validate required fields
        required_fields = ['overall_score', 'strengths', 'weaknesses', 'suggestions']
        missing_fields = [f for f in required_fields if f not in critique]
        if missing_fields:
            raise ParserError(f"Missing required fields: {missing_fields}")
        
        # Add defaults for optional fields
        critique.setdefault('artistic_merit', 0)
        critique.setdefault('technical_feasibility', 0)
        critique.setdefault('cultural_sensitivity', 0)
        critique.setdefault('market_potential', 0)
        critique.setdefault('detailed_analysis', '')
        
        return critique
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise ParserError(f"Failed to parse JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected parsing error: {e}")
        raise ParserError(f"Failed to parse response: {str(e)}")


def parse_style_dna(raw_response: str) -> Dict[str, Any]:
    """
    Parse raw LLM response into structured style DNA.
    
    Args:
        raw_response: Raw text response from Watsonx
        
    Returns:
        Style DNA dictionary
        
    Raises:
        ParserError: If parsing fails
    """
    try:
        json_text = extract_json_from_text(raw_response)
        style_dna = json.loads(json_text)
        
        if not isinstance(style_dna, dict):
            raise ParserError("Response is not a JSON object")
        
        # Add defaults for optional fields
        style_dna.setdefault('style_name', 'Unknown')
        style_dna.setdefault('period', 'Unknown')
        style_dna.setdefault('cultural_origin', 'Unknown')
        style_dna.setdefault('characteristics', [])
        style_dna.setdefault('color_palette', [])
        style_dna.setdefault('techniques', [])
        style_dna.setdefault('mood', 'Unknown')
        style_dna.setdefault('similar_artists', [])
        style_dna.setdefault('key_elements', [])
        
        return style_dna
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        raise ParserError(f"Failed to parse JSON: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected parsing error: {e}")
        raise ParserError(f"Failed to parse response: {str(e)}")


def safe_parse(raw_response: str, parser_func) -> Optional[Any]:
    """
    Safely parse response with error handling.
    
    Args:
        raw_response: Raw text response
        parser_func: Parser function to use
        
    Returns:
        Parsed result or None if parsing fails
    """
    try:
        return parser_func(raw_response)
    except ParserError as e:
        logger.error(f"Parser error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during safe parse: {e}")
        return None

# Made with Bob
