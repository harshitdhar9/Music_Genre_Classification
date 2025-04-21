from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import youtube

app = FastAPI()

# CORS settings: allow all origins (you can restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(youtube.router)
