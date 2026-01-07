from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, Boolean, ForeignKey
from database import Base

class IntentType(str, Enum):
    OPEN_TO_WORK = "OPEN_TO_WORK"
    SCOUTING = "SCOUTING"

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True) # UUID
    username = Column(String, unique=True, index=True)
    global_reputation_score = Column(Float, default=0.0)
    reputation_stake_balance = Column(Integer, default=100)
    is_seed = Column(Boolean, default=False)

class TrustEdge(Base):
    __tablename__ = "trust_edges"
    id = Column(String, primary_key=True, index=True) # UUID
    source_id = Column(String, ForeignKey("users.id"))
    target_id = Column(String, ForeignKey("users.id"))
    skill_tag = Column(String) # e.g. "Python"
    weight = Column(Float, default=1.0) # 0.0 to 1.0 logic
    timestamp = Column(DateTime, default=datetime.utcnow)

# --- SQL TABLE DEFINITION ---
class SkillSignalDB(Base):
    __tablename__ = "skill_signals"

    agent_id = Column(String, primary_key=True, index=True)
    # Link to the User table (Phase 2 integration)
    user_id = Column(String, ForeignKey("users.id"), nullable=True) 
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
