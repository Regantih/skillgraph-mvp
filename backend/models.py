from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, JSON
from database import Base

class IntentType(str, Enum):
    OPEN_TO_WORK = "OPEN_TO_WORK"
    SCOUTING = "SCOUTING"

# --- SQL TABLE DEFINITION ---
class SkillSignalDB(Base):
    __tablename__ = "skill_signals"

    agent_id = Column(String, primary_key=True, index=True)
    intent = Column(String)
    verified_vectors = Column(JSON) # Stores {"Python": 0.9} as JSON
    learning_velocity = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- PYDANTIC MODELS (API) ---
class SkillSignal(BaseModel):
    agent_id: UUID = Field(default_factory=uuid4)
    intent: IntentType
    verified_vectors: Dict[str, float]
    learning_velocity: float
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True
