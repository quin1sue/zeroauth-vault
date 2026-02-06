import os
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from src.database import get_db
from src.model import User

router = APIRouter(prefix="/auth", tags=["auth"])

# You'll get this from your Google Cloud Console
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

@router.post("/google")
async def google_auth(payload: dict, db: Session = Depends(get_db)):
    token = payload.get("id_token")
    if not token:
        raise HTTPException(status_code=400, detail="Missing Google token")

    try:
        # 1. Verify the token with Google's servers
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        email = idinfo['email']
        google_id = idinfo['sub'] # Unique Google ID

        # 2. Check if user exists in our fresh DB
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # 3. NEW USER: This is where the Zero-Knowledge magic starts
            # We generate a unique salt for their Master Key derivation
            new_salt = secrets.token_hex(16)
            
            user = User(
                email=email,
                google_id=google_id,
                is_oauth=True,
                vault_salt=new_salt
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # 4. Return the data the frontend needs to "bake" the Master Key
        return {
            "message": "Login successful",
            "vault_salt": user.vault_salt, 
            "email": user.email,
            "access_token": "mock_jwt_token" # We can add real JWTs later
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Token")