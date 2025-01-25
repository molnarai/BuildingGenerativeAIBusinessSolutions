import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from utils.security import ldap_search_user, ldap_verify_user
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio
from pprint import pprint


router = APIRouter()

@router.get('/problems') 
async def get_problems(db: AsyncSession = Depends(get_db)):
    problems = await db.execute(text("SELECT * FROM problems"))
    results = problems.fetchall()
    # pprint(results)
    # return {'problems': problems}
    # Convert SQLAlchemy result to dict with proper datetime handling
    problems_list = [
        {
            key: value.isoformat() if isinstance(value, (datetime, date)) else value
            for key, value in row._mapping.items()
        }
        for row in results
    ]
    return {'problems': problems_list}


@router.get('/problems/{problem_id}')
async def get_problem_by_id(problem_id: int, db: AsyncSession = Depends(get_db)):
    print(f"Fetching problem with ID {problem_id}...")
    problem = await db.execute(text("SELECT * FROM problems WHERE id = :id"), {"id": problem_id})
    row = problem.fetchone()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    prob = {
        key: value.isoformat() if isinstance(value, (datetime, date)) else value
        for key, value in row._mapping.items()
    }
    return {'problem': prob}


# route to create a new problem
@router.put('/problems/new')
async def create_problem(request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    title = data.get('title')
    description = data.get('description')
    number_of_required_responses = data.get('number_of_required_responses')
    if not title or not description or not number_of_required_responses:
        raise HTTPException(status_code=400, detail="Missing required fields")
    await db.execute(text("INSERT INTO problems (title, description, number_of_required_responses) VALUES (:title, :description, :number_of_required_responses)"), {"title": title, "description": description, "number_of_required_responses": number_of_required_responses})
    await db.commit()
    return {'message': 'Problem created successfully'}

# route to update a problem
@router.put('/problems/{problem_id}')
async def update_problem(problem_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    title = data.get('title')
    description = data.get('description')
    number_of_required_responses = data.get('number_of_required_responses')
    if not title or not description or not number_of_required_responses:
        raise HTTPException(status_code=400, detail="Missing required fields")
    await db.execute(text("UPDATE problems SET title = :title, description = :description, number_of_required_responses = :number_of_required_responses WHERE id = :id"), {"title": title, "description": description, "number_of_required_responses": number_of_required_responses, "id": problem_id})
    await db.commit()
    return {'message': 'Problem updated successfully'}
# route to delete a problem

@router.delete('/problems/{problem_id}')
async def delete_problem(problem_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(text("DELETE FROM problems WHERE id = :id"), {"id": problem_id})
    await db.commit()
    return {'message': 'Problem deleted successfully'}

# route to get all responses for a problem
@router.get('/problems/{problem_id}/responses')
async def get_responses(problem_id: int, db: AsyncSession = Depends(get_db)):
    responses = await db.execute(text("SELECT * FROM responses WHERE problem_id = :problem_id"), {"problem_id": problem_id})
    responses = responses.fetchall()
    return {'responses': responses}
# return {'message': 'Responses retrieved successfully'}

# route to get all responses for a user
@router.get('/users/{user_id}/responses')
async def get_responses(user_id: int, db: AsyncSession = Depends(get_db)):
    responses = await db.execute(text("SELECT * FROM responses WHERE user_id = :user_id"), {"user_id": user_id})
    responses = responses.fetchall()
    return {'responses': responses}
# return {'message': 'Responses retrieved successfully'}

# route to get all responses for a user and problem
@router.get('/users/{user_id}/problems/{problem_id}/responses')
async def get_responses(user_id: int, problem_id: int, db: AsyncSession = Depends(get_db)):
    responses = await db.execute(text("SELECT * FROM responses WHERE user_id = :user_id AND problem_id = :problem_id"), {"user_id": user_id, "problem_id": problem_id})
    responses = responses.fetchall()
    return {'responses': responses}
# return {'message': 'Responses retrieved successfully'}

# route to create a new response
@router.post('/users/{user_id}/problems/{problem_id}/responses')
async def create_response(user_id: int, problem_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    response_text = data.get('response_text')
    if not response_text:
        raise HTTPException(status_code=400, detail="Missing required fields")
    await db.execute(text("INSERT INTO responses (user_id, problem_id, response_text) VALUES (:user_id, :problem_id, :response_text)"), {"user_id": user_id, "problem_id": problem_id, "response_text": response_text})
    await db.commit()
    return {'message': 'Response created successfully'}
# return {'message': 'Response created successfully'}
# route to update a response
@router.put('/users/{user_id}/problems/{problem_id}/responses/<int:response_id>')
async def update_response(user_id: int, problem_id: int, response_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    data = await request.json()
    response_text = data.get('response_text')
    if not response_text:
        raise HTTPException(status_code=400, detail="Missing required fields")
    await db.execute(text("UPDATE responses SET response_text = :response_text WHERE id = :id AND user_id = :user_id AND problem_id = :problem_id"), {"response_text": response_text, "id": response_id, "user_id": user_id, "problem_id": problem_id})
    await db.commit()
    return {'message': 'Response updated successfully'}
# route to delete a response
@router.delete('/users/{user_id}/problems/{problem_id}/responses/<int:response_id>')
async def delete_response(user_id: int, problem_id: int, response_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(text("DELETE FROM responses WHERE id = :id AND user_id = :user_id AND problem_id = :problem_id"), {"id": response_id, "user_id": user_id, "problem_id": problem_id})
    await db.commit()
    return {'message': 'Response deleted successfully'}

# route to get all responses for a user
@router.get('/users/{user_id}/problems/{problem_id}/responses')
async def get_responses(user_id: int, problem_id: int, db: AsyncSession = Depends(get_db)):
    response = await db.execute(text("SELECT * FROM responses WHERE user_id = :user_id AND problem_id = :problem_id"), {"user_id": user_id, "problem_id": problem_id})
