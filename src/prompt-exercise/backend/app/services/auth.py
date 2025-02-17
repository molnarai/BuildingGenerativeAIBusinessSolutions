from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.auth import User, AuthToken, ClientData
from utils.security import get_password_hash, verify_password, ldap_search_user, ldap_verify_user
import os
from concurrent.futures import ThreadPoolExecutor
import asyncio

async def create_user(db: AsyncSession, username: str, password: str, email: str):
    user = User(
        username=username,
        password_hash=get_password_hash(password),
        email=email
    )
    db.add(user)
    await db.commit()
    return user

async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return False
    
    if not verify_password(password, user.password_hash):
        return False
    return user


async def authenticate_user_by_ldap(db: AsyncSession, username: str, password: str):
    # Run synchronous LDAP verification in a thread pool
    with ThreadPoolExecutor() as executor:
        # result = await ldap_verify_user(username, password)
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            ldap_verify_user,
            username,
            password
        )
    if not result:
        return False
    
    db_result = await db.execute(select(User).where(User.username == username))
    db_user = db_result.scalars().first()
    if not db_user:
        new_user = User(
            username=username,
            password_hash=get_password_hash(password),
            email="",
            is_active=True
        )
        db.add(new_user)
        await db.commit()
        return new_user
    else:
        return db_user


async def get_user_by_token(db: AsyncSession, token: str):
    result = await db.execute(select(AuthToken).where(AuthToken.access_token == token))
    token = result.scalars().first()
    if not token:
        return None
    if token.is_revoked or token.expires_at < datetime.now(datetime.timezone.utc):
        return None
    result = await db.execute(select(User).where(User.id == token.user_id))
    return result.scalars().first()


async def revoke_token(db: AsyncSession, token: str):
    result = await db.execute(select(AuthToken).where(AuthToken.access_token == token))
    token = result.scalars().first()
    if token:
        token.is_revoked = True
        await db.commit()


async def create_tokens(db: AsyncSession, user_id: int):
    access_token = os.urandom(24).hex()
    refresh_token = os.urandom(24).hex()
    expires_at = datetime.now(timezone.utc) + timedelta(weeks=4)
    
    token = AuthToken(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(token)
    await db.commit()
    
    return access_token, refresh_token
