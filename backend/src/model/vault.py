from sqlalchemy import Column, String, ForeignKey
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database import Base

class VaultItem(Base):
    __tablename__ = "vault_items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    key_id = Column(UUID(as_uuid=True), ForeignKey("keys.id")) # Which key locked this?
    
    # Metadata
    site_name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    
    encrypted_username = Column(String, nullable=False)
    encrypted_password = Column(String, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="vault_items")
    key = relationship("Key")