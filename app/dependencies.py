from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app import crud
from app.security import decode_access_token

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    # Keep the remaining JWT verification logic unchanged

    # Step 1: Verify and decode JWT
    try:
        payload = decode_access_token(token)

        # Step 2: Extract user ID
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication token"
            )

        user_id = int(user_id)

    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Step 3: Retrieve user from database
    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    # Step 4: Check account status
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    return user
