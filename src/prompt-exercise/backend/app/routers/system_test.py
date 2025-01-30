import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
from utils.security import ldap_search_user, ldap_verify_user
import datetime
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import asyncio


router = APIRouter()

# this route returns a json object with the message "Hello World"
@router.get("/test/hello")
async def hello_world():
    return {"message": "Hello World"}


@router.get("/test/current_time")
async def test_current_time():
    return {"message": f"{datetime.datetime.now()}"}


@router.get("/test/db")
async def test_db(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        # Execute a simple query to check the database connection
        await db.execute(text("SELECT 1"))
        return {"message": "Database connection is working"}
    except Exception as e:
        # If an exception occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


@router.get("/test/dbnow")
async def test_dbnow(request: Request, db: AsyncSession = Depends(get_db)):
    try:
        # Execute a simple query to check the database connection
        result = await db.scalar(text("SELECT NOW()::text"))
        return {
            "message": "Database connection is working"
            , "now_str": str(result)
            , "now_type": str(type(result))
        }
    except Exception as e:
        # If an exception occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


from concurrent.futures import ThreadPoolExecutor
from functools import partial

# @router.post("/test/ldap")
# async def test_ldap_login(request: Request, login_data: dict):
#     try:
#         with ThreadPoolExecutor() as executor:
#             user_info = await asyncio.get_event_loop().run_in_executor(
#                 executor,
#                 partial(
#                     ldap_search_user,
#                     login_data["username"],
#                     login_data["password"]
#                 )
#             )
#             print(f"User info: {user_info}")
        
#         if user_info:
#             return {
#                 "status": "success",
#                 "user_info": user_info
#             }
#         return {
#             "status": "failed",
#             "message": "User not found or invalid credentials"
#         }
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"LDAP error: {str(e)}"
#         )


@router.post("/test/ldap")
def test_ldap_login(request: Request, login_data: dict):
    if True: #try:
        assert os.environ['LDAP_SERVER_URI'] == 'ldap://10.230.100.236', "LDAP server URI is incorrect"
        assert os.environ['LDAP_BASE_DN'] == 'dc=insight,dc=gsu,dc=edu', "LDAP bind DN is incorrect"

        username = login_data["username"]
        password = login_data["password"]
        print(f"testing: {username}")
        print(f"testing: {password}")
        print(f"testing: {os.environ['LDAP_SERVER_URI']}")
        print(f"testing: {os.environ['LDAP_BASE_DN']}")


        # Check if the user exists in LDAP
        # user_exists = ldap_verify_user(username, password)
        # print(f"User {username} exists in LDAP: {user_exists}")
        user_info = ldap_search_user(username, password)
        print(f"User {username} info: {user_info}")

     

        # if user_info:
        #     return {
        #         "status": "success",
        #         "user_info": user_info
        #     }
        return {
            "status": "unknown",
            "message": "Testing" # "User not found or invalid credentials"
        }
    if False: # except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LDAP error: {str(e)}"
        )


# @router.post("/test/ldap/info")
# async def test_ldap_login(request: Request, login_data: dict, db: AsyncSession = Depends(get_db)):
#     try:
#         # Execute a simple query to check the database connection
#         user_name = login_data["username"]
#         user_password = login_data["password"]
#         print(f"testing: {user_name}")
#         success = await ldap_verify_user(user_name, user_password)
#         user_info = await ldap_search_user(login_data["username"], login_data["password"])
       
#         return {
#             "message": "LDAP connection is working",
#             "result": user_info
#         }
#     except Exception as e:
#         # If an exception occurs, raise an HTTPException with a 500 status code
#         raise HTTPException(status_code=500, detail=f"LDAP connection error: {str(e)}")
