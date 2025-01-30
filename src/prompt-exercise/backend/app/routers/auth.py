from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services import auth as auth_service
from models.auth import User
from utils.security import security

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
    return tokens


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