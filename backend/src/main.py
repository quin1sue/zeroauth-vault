from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .model import Key, User
from .database import Base, engine, SessionLocal, get_db
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.config import settings
from src.schema import GoogleAuthRequest
from google.oauth2 import id_token
from google.auth.transport import requests
from src.auth import create_access_token
from src.config import settings
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/auth/google")
def google_auth(token_data: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        idinfo = id_token.verify_oauth2_token(
            token_data.id_token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        google_id = idinfo['sub']
        email = idinfo['email']

        user = db.query(User).filter(User.google_id == google_id).first()

        if not user:
            new_user = User(
                email=email,
                google_id=google_id,
                is_oauth=True
            )
            db.add(new_user)
            db.flush()

            new_key = Key(
                user_id=new_user.id,
                public_key=token_data.public_key,
                device_name=token_data.device_name
            )
            db.add(new_key)
            db.commit()
            db.refresh(new_user)

            # after account creation or login
            access_token = create_access_token(data={"sub": str(user.id)})

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user
                }
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google Authentication")
    



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # decode the token using secret key
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user