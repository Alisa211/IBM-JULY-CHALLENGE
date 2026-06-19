from typing import Dict, Any

class CritiqueAggregator:
    @staticmethod
    def aggregate(critiques: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes the results of the 4 personas and computes a unified response.
        """
        scores = [c["score"] for c in critiques.values()]
        overall_score = sum(scores) / len(scores) if scores else 0.0
        
        all_strengths = []
        all_weaknesses = []
        for c in critiques.values():
            all_strengths.extend(c.get("strengths", []))
            all_weaknesses.extend(c.get("weaknesses", []))
            
        return {
            "overall_score": round(overall_score, 1),
            "top_strengths": list(set(all_strengths))[:5],
            "top_issues": list(set(all_weaknesses))[:5],
            "recommended_revision": "Based on the critique, focus on improving the base geometry for structural integrity while enriching the era-specific iconography."
        }
