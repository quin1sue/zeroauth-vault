from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    salt = Column(String, nullable=False)
    
    # OAuth Fields
    google_id = Column(String, unique=True, index=True, nullable=True)
    is_oauth = Column(Boolean, default=False)

    # Relationships
    vault_items = relationship("VaultItem", back_populates="owner")