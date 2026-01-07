from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from models import SkillSignal, IntentType

app = FastAPI()

# ENABLE CORS FOR VERCEL
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MOCK DB
ACTIVE_MARKET_DB = [
    SkillSignal(
        intent=IntentType.OPEN_TO_WORK,
        verified_vectors={"Python": 0.95, "AI/LLMs": 0.88, "System Arch": 0.85},
        learning_velocity=2.4
    ),
    SkillSignal(
        intent=IntentType.OPEN_TO_WORK,
        verified_vectors={"React": 0.6, "Design": 0.4},
        learning_velocity=1.1
    )
]

@app.get("/")
def read_root():
    return {"status": "SkillGraph Agent Brain Online"}

@app.get("/market/scout", response_model=List[SkillSignal])
async def scout_talent(
    required_skill: str = Query(..., description="Skill to search"),
    min_confidence: float = 0.5
):
    matches = []
    for signal in ACTIVE_MARKET_DB:
        if required_skill in signal.verified_vectors:
            if signal.verified_vectors[required_skill] >= min_confidence:
                matches.append(signal)
    return matches
