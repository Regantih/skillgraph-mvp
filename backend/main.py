from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session
from models import SkillSignal, IntentType, SkillSignalDB
from database import engine, Base, get_db

# Create Tables (Auto-migration for simple schema)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ENABLE CORS FOR VERCEL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "SkillGraph Agent Brain Online (SQL Connected)"}

@app.get("/market/scout", response_model=List[SkillSignal])
async def scout_talent(
    required_skill: str = Query(..., description="Skill to search"),
    min_confidence: float = 0.5,
    db: Session = Depends(get_db)
):
    # Fetch all signals (Optimized: Filter in DB in V2 with Postgres JSONB queries)
    # For now, we fetch all and filter in python to match logic, 
    # but strictly, you should do db.query(SkillSignalDB).filter(...)
    all_signals = db.query(SkillSignalDB).all()
    
    matches = []
    for signal in all_signals:
        vectors = signal.verified_vectors
        if required_skill in vectors:
            if vectors[required_skill] >= min_confidence:
                # Convert DB model to Pydantic
                matches.append(SkillSignal.model_validate(signal))
    return matches

from models import User, TrustEdge # Import new models
from core.trust_engine import TrustEngine
from fastapi import HTTPException
from pydantic import BaseModel

# ... (Existing code) ...

class VerificationRequest(BaseModel):
    verifier_id: str
    candidate_id: str
    skill: str
    stake_amount: int

@app.post("/verify/stake")
def stake_verification(request: VerificationRequest, db: Session = Depends(get_db)):
    """
    Core Trust Mechanism:
    A Verifier stakes reputation to vouch for a Candidate's skill.
    """
    # 1. Check for Duplicate (Sybil Resistance Step 1)
    existing_edge = db.query(TrustEdge).filter(
        TrustEdge.source_id == request.verifier_id,
        TrustEdge.target_id == request.candidate_id,
        TrustEdge.skill_tag == request.skill
    ).first()
    
    if existing_edge:
        raise HTTPException(status_code=400, detail="You have already verified this candidate for this skill.")

    # 2. Check Stake Balance (Skin-in-the-game)
    verifier = db.query(User).filter(User.id == request.verifier_id).first()
    if not verifier:
        # Auto-create for MVP demo if missing (remove in Prod)
        verifier = User(id=request.verifier_id, username="verifier_demo", reputation_stake_balance=100)
        db.add(verifier)
        db.commit()
        db.refresh(verifier)
        
    if verifier.reputation_stake_balance < request.stake_amount:
         raise HTTPException(status_code=402, detail="Insufficient Reputation Stake Balance.")

    # 3. Create the Trust Edge
    new_edge = TrustEdge(
        id=str(uuid4()),
        source_id=request.verifier_id,
        target_id=request.candidate_id,
        skill_tag=request.skill,
        weight=1.0 # Default weight, can be modulated by stake amount
    )
    
    # 4. Deduct Stake
    verifier.reputation_stake_balance -= request.stake_amount
    
    db.add(new_edge)
    db.commit()
    
    return {"status": "Verification Staked", "new_balance": verifier.reputation_stake_balance}

@app.get("/trust/graph")
def get_trust_graph(db: Session = Depends(get_db)):
    """
    Returns the Network Graph for Visualization.
    Nodes: Users (Agents/Verifiers)
    Edges: Trust Verifications
    """
    users = db.query(User).all()
    edges = db.query(TrustEdge).all()
    
    # If empty (Start of Universe), return seed demo data
    if not users:
        return {
            "nodes": [
                {"id": "A", "label": "Alice (Verifier)", "type": "verifier"},
                {"id": "B", "label": "Bob (Agent)", "type": "agent"},
                {"id": "C", "label": "Charlie (Expert)", "type": "verifier"}
            ],
            "edges": [
                {"source": "A", "target": "B", "label": "Python"},
                {"source": "C", "target": "B", "label": "System Arch"}
            ]
        }
    
    return {
        "nodes": [{"id": u.id, "label": u.username or u.id[:8], "type": "verifier" if u.reputation_stake_balance > 0 else "agent"} for u in users],
        "edges": [{"source": e.source_id, "target": e.target_id, "label": e.skill_tag} for e in edges]
    }

from core.gap_analysis import GapAnalysisEngine

class CareerAnalysisRequest(BaseModel):
    user_vectors: Dict[str, float]
    target_role: str # "Senior Python Dev", "ML Engineer"

@app.post("/career/analyze")
def analyze_career_gap(request: CareerAnalysisRequest):
    """
    Career Guide Engine:
    Calculates the 'Skill Gap' between you and industry standards.
    Returns actionable insights (e.g., 'Learn PyTorch').
    """
    # 1. Simulate Market Demand Vectors (In Prod, this comes from live job market data)
    market_profiles = {
        "Senior Python Dev": {"Python": 0.9, "System Arch": 0.8, "Django": 0.7, "SQL": 0.6},
        "ML Engineer": {"Python": 0.9, "AI/LLMs": 0.9, "TensorFlow/PyTorch": 0.8, "Math": 0.7},
        "Frontend Lead": {"React": 0.9, "TypeScript": 0.8, "Design": 0.7, "CSS": 0.8}
    }
    
    target_vector = market_profiles.get(request.target_role)
    if not target_vector:
         raise HTTPException(status_code=404, detail=f"Role '{request.target_role}' not data-mined yet. Try 'Senior Python Dev' or 'ML Engineer'.")
         
    # 2. Run Engine
    analysis = GapAnalysisEngine.analyze_gap(request.user_vectors, target_vector)
    
    return {
        "target_role": request.target_role,
        "analysis": analysis
    }

# BOOTSTRAP ENDPOINT TO SEED DATA (Since we removed the mock list)
@app.post("/seed")
def seed_data(db: Session = Depends(get_db)):
    if db.query(SkillSignalDB).first():
        return {"message": "Data already seeded"}
        
    seeds = [
        SkillSignalDB(
            agent_id="550e8400-e29b-41d4-a716-446655440000",
            intent=IntentType.OPEN_TO_WORK,
            verified_vectors={"Python": 0.95, "AI/LLMs": 0.88, "System Arch": 0.85},
            learning_velocity=2.4
        ),
        SkillSignalDB(
            agent_id="550e8400-e29b-41d4-a716-446655440001",
            intent=IntentType.OPEN_TO_WORK,
            verified_vectors={"React": 0.6, "Design": 0.4},
            learning_velocity=1.1
        )
    ]
    db.add_all(seeds)
    db.commit()
    return {"message": "Seeded 2 agents"}
