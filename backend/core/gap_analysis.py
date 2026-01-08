import math
from typing import Dict, List, Any

class GapAnalysisEngine:
    @staticmethod
    def calculate_euclidean_distance(user_vector: Dict[str, float], target_vector: Dict[str, float]) -> float:
        """
        Calculates the 'Distance' between a user's skills and a target role.
        Lower distance = Better fit.
        """
        # Union of all skills involved
        all_skills = set(user_vector.keys()) | set(target_vector.keys())
        sum_sq = 0.0
        
        for skill in all_skills:
            u_val = user_vector.get(skill, 0.0)
            t_val = target_vector.get(skill, 0.0)
            sum_sq += (u_val - t_val) ** 2
            
        return math.sqrt(sum_sq)

    @staticmethod
    def analyze_gap(user_vector: Dict[str, float], target_role_vector: Dict[str, float]) -> Dict[str, Any]:
        """
        Analyzes the gap between a user and a target role.
        Returns fit score, distance, and actionable insights (gaps).
        """
        distance = GapAnalysisEngine.calculate_euclidean_distance(user_vector, target_role_vector)
        
        gaps = []
        strengths = []
        
        for skill, target_score in target_role_vector.items():
            user_score = user_vector.get(skill, 0.0)
            diff = target_score - user_score
            
            if diff > 0.15: # Significant gap threshold
                priority = "HIGH" if diff > 0.4 else "MEDIUM"
                gaps.append({
                    "skill": skill, 
                    "current": user_score, 
                    "target": target_score,
                    "gap": round(diff, 2), 
                    "priority": priority
                })
            elif diff < -0.1:
                strengths.append(skill)
                
        # Normalize distance to a 0-100 fit score (Approximate heuristic)
        # Assuming max reasonable distance is ~2.0 for normalized 0-1 vectors
        fit_score = max(0, 1.0 - (distance / 2.5)) * 100
        
        return {
            "role_fit_score": round(fit_score, 1),
            "euclidean_distance": round(distance, 4),
            "identified_gaps": sorted(gaps, key=lambda x: x['gap'], reverse=True),
            "strengths": strengths
        }
