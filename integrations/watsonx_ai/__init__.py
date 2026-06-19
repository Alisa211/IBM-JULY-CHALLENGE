"""
Watsonx.ai Integration Package

Contains clients, prompts, and parsers for IBM Watsonx.ai integration.
"""

from integrations.watsonx_ai.clients import WatsonxClient, get_watsonx_client
from integrations.watsonx_ai.prompts import (
    IDEA_GENERATION_PROMPT,
    CRITIQUE_PROMPT,
    STYLE_DNA_PROMPT,
    format_prompt
)
from integrations.watsonx_ai.parser import (
    parse_idea_cards,
    parse_critique,
    parse_style_dna,
    ParserError
)

__all__ = [
    'WatsonxClient',
    'get_watsonx_client',
    'IDEA_GENERATION_PROMPT',
    'CRITIQUE_PROMPT',
    'STYLE_DNA_PROMPT',
    'format_prompt',
    'parse_idea_cards',
    'parse_critique',
    'parse_style_dna',
    'ParserError',
]

# Made with Bob
