from typing import List, Optional

def build_embedding_text_from_vision(
    iconography: List[str], 
    motifs: List[str], 
    style_traits: List[str],
    deity: Optional[str] = None,
    tradition: Optional[str] = None,
    region: Optional[str] = None
) -> str:
    """
    Constructs a semantic string from structured vision outputs to be embedded and searched.
    """
    parts = []
    if deity:
        parts.append(f"Depicts the deity {deity}.")
    if tradition:
        parts.append(f"Belongs to the {tradition} tradition.")
    if region:
        parts.append(f"Originates from {region}.")
    if iconography:
        parts.append(f"Features {', '.join(iconography)}.")
    if motifs:
        parts.append(f"Contains motifs like {', '.join(motifs)}.")
    if style_traits:
        parts.append(f"Stylistically {', '.join(style_traits)}.")
        
    return " ".join(parts)
