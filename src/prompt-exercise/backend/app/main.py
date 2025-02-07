import os
from fastapi.encoders import jsonable_encoder
from datetime import datetime, date
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from routers import auth, ai_chat
from database import engine, Base, create_tables, create_async_engine
from routers import (
    assignment,
    auth,
    system_test,
    ai_chat,
)
from models import auth as auth_model
from models import assignment as assignment_model

class CustomJSONEncoder:
    def encode_datetime(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(assignment.router, prefix="/assignment", tags=["assignment"])
app.include_router(ai_chat.router, tags=["ai"])
app.include_router(system_test.router, tags=["system"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await create_tables()
        await conn.run_sync(Base.metadata.create_all)


@app.middleware("http")
async def custom_json_middleware(request, call_next):
    response = await call_next(request)
    if isinstance(response, JSONResponse):
        response.body = jsonable_encoder(
            response.body,
            custom_encoder={
                datetime: lambda dt: dt.isoformat(),
                date: lambda d: d.isoformat()
            }
        )
    return response


@app.get("/")
async def index_page():
    return {"message": "Index Page"}

def print_environments():
    for key, value in os.environ.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    print_environments()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
