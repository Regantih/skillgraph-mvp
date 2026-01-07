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
