# main.py

from contextlib import asynccontextmanager
from app.main import api_router
from .utils.db import create_db_and_tables
from fastapi import FastAPI , Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import json



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    yield
    


app = FastAPI(lifespan=lifespan, 
    title="Nextjs todo app with fastapi", 
    version="0.0.1",
    servers=[
        # Localhost server
        {
            "url": "http://127.0.0.1:8000/", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        },
         {
            "url": "http://localhost:8000/", # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        },
    ]
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


# @app.post("/cookie/")
# def create_cookie():
#     content = {"message": "Cookie created successfully"}
#     response = Response(content=json.dumps(content))  # Convert content to JSON string
#     response.set_cookie(key="fakesession", value="fake-cookie-session-value", max_age=3600, httponly=True)
#     return response