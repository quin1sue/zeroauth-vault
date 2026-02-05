from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class KeyBase(BaseModel):
    public_key: str
    device_name: str = "Web Browser"

class KeyResponse(KeyBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: Optional[str] = None # Plain text for the 'Front Door' hashing
    public_key: str                # The 'Lock' for the vault
    device_name: str = "Initial Device"

# What the server sends back (Never send back the password!)
class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_oauth: bool
    keys: List[KeyResponse] = [] # Shows the user their registered devices

    class Config:
        from_attributes = True

# What the frontend sends when saving a new password
class VaultItemCreate(BaseModel):
    site_name: str
    url: Optional[str] = None
    encrypted_username: str
    encrypted_password: str
    key_id: UUID # The ID of the public key used to lock this item

class VaultItemResponse(VaultItemCreate):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

class GoogleAuthRequest(BaseModel):
    id_token: UUID
    public_key: Optional[str] = None
    device_name: str = "Web Browser"