from datetime import datetime, timedelta, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel

SECRET_KEY = "change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 300

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
    if payload.username != "admin" or payload.password != "admin123":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": _create_token(payload.username),
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }


@app.post("/token/refresh")
def refresh_token(payload: RefreshRequest):
    try:
        decoded = jwt.decode(payload.token, SECRET_KEY, algorithms=[ALGORITHM])
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
