from typing import Dict, Any, List

class StyleDNAGenerator:
    """
    Converts extracted vision JSON into a set of numerical vectors (for pgvector embedding)
    and textual style traits for prompt context.
    """
    
    @staticmethod
    def generate_style_dna(extracted_json: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns numerical scores and text traits based on the structured JSON.
        """
        iconography = [i.lower() for i in extracted_json.get("iconography", [])]
        motifs = [m.lower() for m in extracted_json.get("motifs", [])]
        composition = [c.lower() for c in extracted_json.get("composition", [])]
        form = extracted_json.get("form", "").lower()
        
        # Heuristic scoring to simulate a vector embedding output
        scores = {
            "movement": 0.5,
            "symbolism": 0.5,
            "ornamentation": 0.5,
            "ritual_function": 0.5,
            "material_complexity": 0.5
        }
        
        traits: List[str] = []
        
        # Movement
        if "dance" in form or "dynamic" in " ".join(composition):
            scores["movement"] = 0.95
            traits.append("Kinetic Energy")
        elif "seated" in form or "symmetrical" in " ".join(composition):
            scores["movement"] = 0.20
            traits.append("Classical Balance")
            
        # Symbolism
        if len(iconography) > 2:
            scores["symbolism"] = 0.99
            traits.append("Highly Symbolic")
            
        # Ornamentation
        if "floral" in " ".join(motifs) or "intricate" in " ".join(motifs):
            scores["ornamentation"] = 0.87
            traits.append("Ornate Motif")
            
        # Ritual Function
        if extracted_json.get("deity"):
            scores["ritual_function"] = 0.98
            traits.append("Sacred Function")
            
        # Material Complexity
        materials = [m.lower() for m in extracted_json.get("materials", [])]
        if "bronze" in materials or "metal" in materials:
            scores["material_complexity"] = 0.91
            traits.append("Metallic Craftsmanship")
            
        if not traits:
            traits.append("Traditional Form")
            
        return {
            "vector_scores": scores,
            "style_traits": traits
        }
