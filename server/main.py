import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import api_router


app = FastAPI(
    title="AI Job Matcher",
    description="An AI-powered job matching platform that connects job seekers with their ideal career opportunities.",
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
async def read_root():
    return {"Hello": "Ram"}
