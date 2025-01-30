from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.auth import User, AuthToken, ClientData
from models.assignment import Problem, Response
from services.database import get_db
from utils.security import get_password_hash, verify_password, ldap_search_user, ldap_verify_user
import os
from concurrent.futures import ThreadPoolExecutor
import HttpStatusCode

#   ____            _     _                    
#  |  _ \ _ __ ___ | |__ | | ___ _ __ ___  ___ 
#  | |_) | '__/ _ \| '_ \| |/ _ \ '_ ` _ \/ __|
#  |  __/| | | (_) | |_) | |  __/ | | | | \__ \
#  |_|   |_|  \___/|_.__/|_|\___|_| |_| |_|___/
                                             
async def create_problem(db: AsyncSession, problem_name: str, description: str, num_resp: int):
    new_problem = Problem(name=problem_name, description=description, number_of_required_responses=num_resp)
    db.add(new_problem)
    await db.commit()
    return new_problem


async def delete_problem(db: AsyncSession, problem_id: int):
    problem = await get_problem(db, problem_id)
    if not problem:
        return False
    await db.delete(problem)
    await db.commit()
    return True


async def get_problem(db: AsyncSession, problem_id: int):
    result = await db.execute(select(Problem).where(Problem.id == problem_id))
    return result.scalars().first()


async def get_all_problems(db: AsyncSession):
    result = await db.execute(select(Problem))
    return result.scalars().all()


#   ____                                           
#  |  _ \ ___  ___ _ __   ___  _ __  ___  ___  ___ 
#  | |_) / _ \/ __| '_ \ / _ \| '_ \/ __|/ _ \/ __|
#  |  _ <  __/\__ \ |_) | (_) | | | \__ \  __/\__ \
#  |_| \_\___||___/ .__/ \___/|_| |_|___/\___||___/
#                 |_|                              

async def create_response(db: AsyncSession, user_id: int, problem_id: int, response_text: str):
    new_response = Response(user_id=user_id, problem_id=problem_id, response_text=response_text)
    db.add(new_response)
    await db.commit()
    return new_response

async def get_response(db: AsyncSession, response_id: int):
    result = await db.execute(select(Response).where(Response.id == response_id))
    return result.scalars().first()

async def get_response_by_user_and_problem(db: AsyncSession, user_id: int, problem_id: int):
    result = await db.execute(select(Response).where(Response.user_id == user_id).where(Response.problem_id == problem_id))
    return result.scalars().first()

async def get_all_responses(db: AsyncSession, problem_id: int):
    result = await db.execute(select(Response).where(Response.problem_id == problem_id))
    return result.scalars().all()

async def get_all_responses_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Response).where(Response.user_id == user_id))
    return result.scalars().all()

async def select_response_for_submission(db: AsyncSession, response_id: int, user_id: int):
    result = await db.execute(select(Response)
                              .where(Response.id == response_id)
                              .where(Response.user_id == user_id)
                              .where(Response.selected == False))
    rec = result.scalars().first()
    if not rec:
        return False
    rec.selected = True
    db.commit()
    return rec


async def unselect_response_for_submission(db: AsyncSession, response_id: int, user_id: int):
    result = await db.execute(select(Response)
                              .where(Response.id == response_id)
                              .where(Response.user_id == user_id)
                              .where(Response.selected == True))
    rec = result.scalars().first()
    if not rec:
        return False
    rec.selected = False
    db.commit()
    return rec