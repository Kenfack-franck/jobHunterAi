from sqlalchemy import Column, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class UserFeedCache(Base):
    __tablename__ = "user_feed_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    profile_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    job_offer_id = Column(UUID(as_uuid=True), nullable=False)
    
    compatibility_score = Column(Float, nullable=False)
    calculated_at = Column(DateTime, server_default=func.now(), nullable=False)
    expires_at = Column(DateTime, nullable=False, index=True)
