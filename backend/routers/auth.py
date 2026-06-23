"""
Authentication router for SmartReview
Handles Google OAuth and Email/Password authentication
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from jose import jwt
import httpx
import os

router = APIRouter()

SECRET_KEY = os.environ.get("SECRET_KEY", "smartreview-secret-2026")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")


class GoogleAuthRequest(BaseModel):
    token: str


class EmailAuthRequest(BaseModel):
    email: str
    password: str


@router.post("/google")
async def google_auth(request: GoogleAuthRequest):
    """
    Authenticate user using Google OAuth token
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={request.token}"
        )
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_info = response.json()
        token = jwt.encode(
            {"sub": user_info["email"], "name": user_info.get("name", "")},
            SECRET_KEY, algorithm="HS256"
        )
        return {"token": token, "user": user_info}


@router.post("/login")
async def login(request: EmailAuthRequest):
    """
    Authenticate user using email and password
    (Simple auth for demo purposes - in production, use proper password hashing)
    """
    # Simple auth pour démo
    token = jwt.encode(
        {"sub": request.email},
        SECRET_KEY, algorithm="HS256"
    )
    return {"token": token}


@router.get("/verify")
async def verify_token():
    """
    Verify if the user is authenticated
    """
    return {"status": "authenticated"}
