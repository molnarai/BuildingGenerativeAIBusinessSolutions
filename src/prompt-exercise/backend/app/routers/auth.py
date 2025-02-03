from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import auth as auth_service
from models.auth import User
from utils.security import security
from dependencies import get_current_user


router = APIRouter()

@router.post("/register")
async def register(user_data: dict, db: AsyncSession = Depends(get_db)):
    return await auth_service.create_user(db, user_data["username"], user_data["password"], user_data["email"])


@router.post("/login")
async def login(request: Request, login_data: dict, db: AsyncSession = Depends(get_db)):
    # user = await auth_service.authenticate_user(db, login_data["username"], login_data["password"])
    user = await auth_service.authenticate_user_by_ldap(db, login_data["username"], login_data["password"])
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    tokens = await auth_service.create_tokens(db, user.id)
    return {
        "access_token": tokens[0],
        "refresh_token": tokens[1],
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            # "display_name": user.gecos,
            "email": user.email
        },
        "success": True,
        "message": "Login successful"
    }


@router.post("/token/refresh")
async def refresh_token(request: dict, current_token: str = Depends(security), db: AsyncSession = Depends(get_db)):
    try:
        user_id = await auth_service.validate_refresh_token(db, request.get("refresh_token"))
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        tokens = await auth_service.create_tokens(db, user_id)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token refresh failed")
    

@router.get("/user/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "display_name": current_user.gecos,
        "is_admin": current_user.is_admin,
    }