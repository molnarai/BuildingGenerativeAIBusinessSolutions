from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from database import get_db
from models.auth import AuthToken, User

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    
    # Use select instead of query
    stmt = select(AuthToken).where(
        AuthToken.access_token == token,
        AuthToken.expires_at > datetime.now(timezone.utc)
    )
    
    # Execute the query
    result = await db.execute(stmt)
    db_token = result.scalar_one_or_none()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return {
        "user_id": db_token.user_id,
    }

async def get_current_user(
    token_data: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.id == token_data["user_id"])
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

async def verify_admin(
    token_data: dict = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(User).where(User.id == token_data["user_id"])
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user




# @router.delete("/admin/users/{user_id}")
# async def delete_user(
#     user_id: int,
#     admin: User = Depends(verify_admin)
# ):
#     # Admin-only operation
#     return {"message": "User deleted"}