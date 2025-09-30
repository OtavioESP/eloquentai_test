from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from migration_util import auto_migrate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Chat API",
    description="A FastAPI application for RAG chat functionality with automatic database migrations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """Run database migrations on startup"""
    logger.info("Starting RAG Chat API...")
    
    # Run automatic migrations
    migration_success = auto_migrate()
    
    if migration_success:
        logger.info("✓ Database migrations completed successfully")
    else:
        logger.error("✗ Database migrations failed - API may not function correctly")
        # Note: In production, you might want to exit here or handle this differently
        # For development, we'll continue but log the error

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down RAG Chat API...")
