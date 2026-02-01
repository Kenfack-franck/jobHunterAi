from sqlalchemy import Column, String, Integer, Text, DateTime, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.database import Base


class CustomSource(Base):
    __tablename__ = "custom_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    
    source_name = Column(String(100), nullable=False)
    source_url = Column(String(500), nullable=False)
    source_type = Column(String(50), default="html", nullable=False)  # html, json, unknown
    is_active = Column(Boolean, default=True, nullable=False)
    scraping_frequency = Column(String(20), default="every_4_hours", nullable=False)  # hourly, every_4_hours, daily, weekly
    
    last_scraped_at = Column(DateTime, nullable=True)
    total_offers_found = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
