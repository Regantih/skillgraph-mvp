from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict

class TrustEngine:
    """
    Implements the core Trust Logic for SkillGraph.
    
    Principles (from Master Doc):
    1. Weighted Transitive Trust: Trust flows through verified edges.
    2. Dampening: Trust decays with distance (0.85 factor per hop).
    3. Sybil Resistance: Only nodes reachable from the "Trusted Seed Set" can have non-zero reputation.
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def calculate_global_reputation(self, seed_user_ids: List[str]) -> Dict[str, float]:
        """
        Calculates Global Reputation scores using a Recursive CTE (EigenTrust-lite).
        This executes purely in the SQL engine for performance and robustness.
        
        Args:
            seed_user_ids: List of UUIDs representing the "Trusted Seed Set".
            
        Returns:
            Dict[user_id, trust_score]
        """
        if not seed_user_ids:
            return {}

        # Format seed IDs for SQL IN clause
        seed_list_str = "', '".join(str(uid) for uid in seed_user_ids)
        
        # SQL Logic based on Master Doc Section 3.3
        # Note: We assume a 'trust_edges' table exists with (source_id, target_id, weight)
        query = text(f"""
        WITH RECURSIVE TrustFlow AS (
            -- Anchor: Seed Nodes have trust 1.0 (Base Trust)
            SELECT 
                id as user_id, 
                1.0::float as trust_score, 
                0 as depth
            FROM users 
            WHERE id IN ('{seed_list_str}')
            
            UNION ALL
            
            -- Recursive: Trust flows to neighbors
            SELECT 
                e.target_id, 
                (tf.trust_score * e.weight * 0.85)::float as trust_score,
                tf.depth + 1
            FROM TrustFlow tf
            JOIN trust_edges e ON tf.user_id = e.source_id
            WHERE tf.depth < 6 -- Max 6 degrees of separation to prevent infinite loops
        )
        -- Aggregate scores (Summing paths strengthens reputation)
        SELECT user_id, SUM(trust_score) as final_score 
        FROM TrustFlow 
        GROUP BY user_id
        ORDER BY final_score DESC;
        """)
        
        results = self.db.execute(query).fetchall()
        
        # Convert to Dictionary
        return {str(row[0]): float(row[1]) for row in results}

    def verify_transaction(self, verifier_id: str, candidate_id: str, stake_amount: int):
        """
        Executes a "Staked Verification".
        The Verifier must have enough 'reputation_stake_balance'.
        """
        # Logic to be implemented: Check balance, deduct stake, create edge.
        pass
