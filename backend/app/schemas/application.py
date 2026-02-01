"""Application schemas"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from uuid import UUID


class ApplicationStatus(str, Enum):
    PENDING = "pending"
    REPLIED = "replied"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class ApplicationBase(BaseModel):
    company_name: str = Field(..., max_length=255)
    job_title: str = Field(..., max_length=255)
    email_to: str = Field(..., max_length=255)
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    job_offer_id: Optional[UUID] = None


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: UUID
    user_id: UUID
    job_offer_id: Optional[UUID] = None
    status: str
    documents_sent: Optional[Dict[str, Any]] = None
    applied_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ApplicationStats(BaseModel):
    total: int
    by_status: Dict[str, int]
    response_rate: float
