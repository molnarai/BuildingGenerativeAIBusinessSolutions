import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import text, select
from pydantic import BaseModel, Field
from database import get_db
from utils.security import ldap_search_user, ldap_verify_user
from datetime import datetime, date, timezone
from typing import Optional
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio
from pprint import pprint
import logging

from dependencies import verify_token, get_current_user
from models.auth import User
from models.assignment import Response

logger = logging.getLogger(__name__)

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


#   ____                                    _   ____      _        _                
#  / ___|  __ ___   _____    __ _ _ __   __| | |  _ \ ___| |_ _ __(_) _____   _____ 
#  \___ \ / _` \ \ / / _ \  / _` | '_ \ / _` | | |_) / _ \ __| '__| |/ _ \ \ / / _ \
#   ___) | (_| |\ V /  __/ | (_| | | | | (_| | |  _ <  __/ |_| |  | |  __/\ V /  __/
#  |____/ \__,_| \_/ \___|__\__,_|_| |_|\__,_| |_| \_\___|\__|_|  |_|\___| \_/ \___|
#  | | | |___  ___ _ __  |  _ \ ___  ___ _ __   ___  _ __  ___  ___  ___            
#  | | | / __|/ _ \ '__| | |_) / _ \/ __| '_ \ / _ \| '_ \/ __|/ _ \/ __|           
#  | |_| \__ \  __/ |    |  _ <  __/\__ \ |_) | (_) | | | \__ \  __/\__ \           
#   \___/|___/\___|_|    |_| \_\___||___/ .__/ \___/|_| |_|___/\___||___/           
#                                       |_|                                         

class ResponseData(BaseModel):
    uuid: str = Field(..., description="Unique identifier for the response")
    ai_input_tokens: Optional[int] = None
    ai_max_tokens: Optional[int] = None
    ai_model: Optional[str] = None
    ai_output_tokens: Optional[int] = None
    ai_provider: Optional[str] = None
    ai_seconds: Optional[float] = None
    ai_stream: Optional[bool] = None
    ai_temperature: Optional[float] = None
    ai_timestamp: Optional[str] = None
    llm_answer: Optional[str] = None
    problem_description: Optional[str] = None
    problem_id: Optional[int] = None
    problem_title: Optional[str] = None
    prompt: Optional[str] = None
    select_for_submission: Optional[bool] = None
    user_comment: Optional[str] = None
    username: Optional[str] = None

    class Config:
        extra = "allow"  # Allows extra fields in the input
    

class ResponseResult(BaseModel):
    success: bool
    message: str


@router.post('/responses/save')
async def save_response(
    response_data: ResponseData,
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
) -> ResponseResult:
    try:
        # Log the incoming data for debugging
        logger.info(f"Received response data: {response_data.dict()}")
        logger.info(f"Token data: {token_data}")

        # Get user information
        user_query = select(User).where(User.id == token_data["user_id"])
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()
        
        if not user:
            return ResponseResult(
                success=False,
                message="User not found"
            )

        # Check if response exists
        response_query = select(Response).where(Response.uuid == response_data.uuid)
        result = await db.execute(response_query)
        existing_response = result.scalar_one_or_none()

        current_time = datetime.now(timezone.utc)

        if existing_response:
            # Update existing response, only select_for_submission is allowed
            try:
                logging.info("Updating existing response")
                existing_response.select_for_submission = \
                        response_data.select_for_submission
                existing_response.updated_at = current_time
                await db.commit()
                return ResponseResult(
                    success=True,
                    message="Response updated successfully"
                )
            except Exception as e:
                await db.rollback()
                return ResponseResult(
                    success=False,
                    message=f"Error updating response: {str(e)}"
                )
        else:
            # Create new response
            try:
                logging.info("Creating new response")
                new_response = Response(
                    uuid=response_data.uuid,
                    user_id=user.id,
                    created_at=current_time,
                    updated_at=current_time,
                    ai_input_tokens=response_data.ai_input_tokens,
                    ai_max_tokens=response_data.ai_max_tokens,
                    ai_model=response_data.ai_model,
                    ai_output_tokens=response_data.ai_output_tokens,
                    ai_provider=response_data.ai_provider,
                    ai_seconds=response_data.ai_seconds,
                    ai_stream=response_data.ai_stream,
                    ai_temperature=response_data.ai_temperature,
                    ai_timestamp=response_data.ai_timestamp,
                    llm_answer=response_data.llm_answer,
                    problem_description=response_data.problem_description,
                    problem_id=response_data.problem_id,
                    problem_title=response_data.problem_title,
                    prompt=response_data.prompt,
                    select_for_submission=response_data.select_for_submission
                )
                db.add(new_response)
                await db.commit()
                return ResponseResult(
                    success=True,
                    message="Response created successfully"
                )
            except Exception as e:
                await db.rollback()
                return ResponseResult(
                    success=False,
                    message=f"Error creating response: {str(e)}"
                )
            except Exception as e:
                await db.rollback()
                return ResponseResult(
                    success=False,
                    message=f"Error saving response: {str(e)}"
                )

    except Exception as e:
        return ResponseResult(
            success=False,
            message=f"An unexpected error occurred: {str(e)}"
        )
    
@router.post('/responses/validate')
async def validate_response(response_data: ResponseData):
    """Endpoint to validate the response data format"""
    return {
        "success": True,
        "message": "Data format is valid",
        "received_data": response_data.dict()
    }

@router.get('/responses')
async def load_responses(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
    ):
    try:
        # Log the incoming data for debugging
        logger.info(f"Token data: {token_data}")

        # Get user information
        user_query = select(User).where(User.id == token_data["user_id"])
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()
        
        if not user:
            return ResponseResult(
                success=False,
                message="User not found"
            )

        responses = await db.execute(text("SELECT * FROM responses where user_id = :user_id"),
                                      {"user_id": token_data["user_id"]})
        results = responses.fetchall()
        response_data = [
            {
                key: value.isoformat() if isinstance(value, (datetime, date)) else value
                for key, value in row._mapping.items()
            }
        for row in results
        ]

        return {"success": True, "data": response_data}
    
    except Exception as e:
        return ResponseResult(
            success=False,
            message=f"An unexpected error occurred: {str(e)}"
        )
    

@router.get('/responses/counts')
async def load_responses_counts(
    token_data: dict = Depends(verify_token),
    db: Session = Depends(get_db)
    ):
    try:
        # Log the incoming data for debugging
        logger.info(f"Token data: {token_data}")

        # Get user information
        user_query = select(User).where(User.id == token_data["user_id"])
        result = await db.execute(user_query)
        user = result.scalar_one_or_none()
        
        if not user:
            return ResponseResult(
                success=False,
                message="User not found"
            )

        # Get the counts of each response type
        q = """
            WITH restab AS (
                SELECT r.problem_title, r.problem_id
                , COUNT(r.problem_id) as total_count
                , SUM(CAST(r.select_for_submission as INT)) AS selected_count
                FROM responses r
            
                WHERE r.user_id = :user_id
                GROUP BY r.problem_id, r.problem_title
                ORDER BY r.problem_id
            )
            SELECT p.id AS problem_id, p.title AS problem_title
            , restab.total_count AS total_count
            , restab.selected_count AS selected_count
            , p.number_of_required_responses AS required_count
            FROM restab
            RIGHT JOIN problems p ON restab.problem_id = p.id
            ORDER BY p.id
        """
        query = text(q) 
        responses = await db.execute(query, {"user_id": token_data["user_id"]})
        results = responses.fetchall()
        response_data = [
            {
                key: value.isoformat() if isinstance(value, (datetime, date)) else value
                for key, value in row._mapping.items()
            }
            for row in results
        ]
        logger.info(f"Response data: {response_data}")
        return {"success": True, "data": response_data}
    
    except Exception as e:
        return ResponseResult(
            success=False,
            message=f"An unexpected error occurred: {str(e)}"
        )

        db = SessionLocal()
        responses = db.query(Response).all()