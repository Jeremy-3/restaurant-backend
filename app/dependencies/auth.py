from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid Token")

        logging.info(f"[AUTH] Fetching user with email: {email}")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Extract role and permissions from token
        token_user = payload.get("user", {})
        role_data = token_user.get("role", {})
        role_name = role_data.get("name", "user")
        permissions = role_data.get("permissions", [])

        return {
            "user": user,
            "role_name": role_name,
            "permissions": permissions
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")