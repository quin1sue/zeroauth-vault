from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Hashed password for standard login (null if using ONLY Google OAuth)
    hashed_password = Column(String, nullable=True) 
    
    # OAuth Fields
    google_id = Column(String, unique=True, index=True, nullable=True)
    is_oauth = Column(Boolean, default=False)

    # Relationships
    keys = relationship("Key", back_populates="owner")
    vault_items = relationship("VaultItem", back_populates="owner")