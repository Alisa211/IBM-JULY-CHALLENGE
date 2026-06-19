from typing import Dict, List, Any

WORKFLOW_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "creative_generation": {
        "name": "creative_generation",
        "description": "Standard linear pipeline to generate and critique a creative concept.",
        "steps": [
            "research",
            "style",
            "generate",
            "critique",
            "revise"
        ],
        "pauses_after": [
            "generate" # Example: Wait for human review after generating concepts
        ]
    },
    "style_extraction_only": {
        "name": "style_extraction_only",
        "description": "Only analyze historical context and extract style rules.",
        "steps": [
            "research",
            "style"
        ],
        "pauses_after": []
    }
}

def get_workflow(name: str) -> Dict[str, Any]:
    if name not in WORKFLOW_DEFINITIONS:
        raise ValueError(f"Workflow '{name}' not found.")
    return WORKFLOW_DEFINITIONS[name]

