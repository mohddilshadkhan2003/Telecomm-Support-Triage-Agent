from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("TRIAGE_SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
TOKEN_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "480"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change-me")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(username: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=TOKEN_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def authenticate(username: str, password: str) -> str | None:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return "admin"
    return None


def current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("sub") or not payload.get("role"):
            raise credentials_error
        return payload
    except jwt.PyJWTError as exc:
        raise credentials_error from exc


def require_admin(user: Annotated[dict, Depends(current_user)]) -> dict:
    if user.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrator access required")
    return user
