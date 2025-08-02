from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import tracking, meetings, users, senders_recipients, analytics
from .database import create_tables
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Email Read Tracking API",
    description="A FastAPI service for tracking email read status",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tracking.router)
app.include_router(meetings.router)
app.include_router(users.router)
app.include_router(senders_recipients.router)
app.include_router(analytics.router)

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    create_tables()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Email Read Tracking API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "email-read-tracking"}
