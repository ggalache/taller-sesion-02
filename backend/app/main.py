from datetime import datetime, timedelta, timezone
import os
from secrets import compare_digest
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")
if len(SECRET_KEY) < 32:
    raise RuntimeError("SECRET_KEY must be at least 32 characters long")

app = FastAPI(title="JWT FastAPI Example")


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    token: str


def _create_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    payload = {"sub": subject, "exp": expire, "jti": str(uuid4())}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token")
def create_token(payload: LoginRequest):
    valid_user = compare_digest(payload.username, ADMIN_USERNAME)
    valid_pass = compare_digest(payload.password, ADMIN_PASSWORD)
    if not (valid_user and valid_pass):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": _create_token(payload.username),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }


@app.post("/token/refresh")
def refresh_token(payload: RefreshRequest):
    try:
        decoded = jwt.decode(
            payload.token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": True},
        )
        subject = decoded.get("sub")
        if not subject:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    return {
        "access_token": _create_token(subject),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }
