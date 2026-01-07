from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

class IntentType(str, Enum):
    OPEN_TO_WORK = "OPEN_TO_WORK"
    SCOUTING = "SCOUTING"

class SkillSignal(BaseModel):
    agent_id: UUID = Field(default_factory=uuid4)
    intent: IntentType
    verified_vectors: Dict[str, float]
    learning_velocity: float
    timestamp: datetime = Field(default_factory=datetime.now)
