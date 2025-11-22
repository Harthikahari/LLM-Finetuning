"""
FastAPI application for Text2SQL inference.

Run with: uvicorn api.main:app --reload
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.schemas import PredictionRequest, PredictionResponse, BatchPredictionRequest, HealthResponse
from api.routes import router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create app
app = FastAPI(
    title="Text2SQL API",
    description="Production-grade REST API for converting natural language questions to SQL queries using fine-tuned LLMs",
    version="1.0.0",
    contact={
        "name": "Text2SQL Contributors",
        "url": "https://github.com/Harthikahari/LLM-Finetuning",
        "email": "text2sql@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    logger.info("Starting Text2SQL API")
    # Model loading happens in router


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Text2SQL API")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
