from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from migration_util import auto_migrate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG Chat API",
    description="The Otavio FastAPI application for RAG chat functionality with auto db migrations",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting RAG Chat API...")
    
    migration_success = auto_migrate()
    
    if migration_success:
        logger.info("Database migrations completed successfully")
    else:
        logger.error("Database migrations failed - API may not function correctly")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down RAG Chat API...")
