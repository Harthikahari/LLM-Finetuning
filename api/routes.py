"""API routes for Text2SQL."""

from fastapi import APIRouter, HTTPException, Depends
import logging
import os

from api.schemas import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
    ModelInfo,
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Global model instance (lazy loaded)
_model = None
_predictor = None


def get_model():
    """Get or load model."""
    global _model, _predictor

    if _model is None:
        logger.info("Loading model...")
        model_path = os.getenv("MODEL_PATH", "./outputs")

        try:
            from text2sql.models.model_factory import create_model
            from text2sql.inference.predictor import Text2SQLPredictor

            _model = create_model(model_name=model_path, training_method="lora")
            _predictor = Text2SQLPredictor(
                model=_model,
                tokenizer=_model.tokenizer,
            )
            logger.info(f"Model loaded from {model_path}")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise HTTPException(status_code=500, detail=f"Model loading failed: {e}")

    return _predictor


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        predictor = get_model()
        model_loaded = predictor is not None
    except:
        model_loaded = False

    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        model_loaded=model_loaded,
        version="0.1.0",
    )


@router.get("/model/info", response_model=ModelInfo)
async def model_info(predictor = Depends(get_model)):
    """Get model information."""
    return ModelInfo(
        model_name=predictor.model.model_name_or_path,
        model_type="text2sql",
        parameters=predictor.model.get_num_parameters(),
        device=predictor.device,
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    predictor = Depends(get_model),
):
    """Generate SQL query from natural language question."""
    try:
        queries = predictor.predict(
            question=request.question,
            schema=request.schema,
            num_return_sequences=request.num_return_sequences,
        )

        return PredictionResponse(
            queries=queries,
            question=request.question,
        )

    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def batch_predict(
    request: BatchPredictionRequest,
    predictor = Depends(get_model),
):
    """Batch prediction endpoint."""
    try:
        queries = predictor.batch_predict(
            questions=request.questions,
            schemas=request.schemas,
        )

        return BatchPredictionResponse(
            queries=queries,
            count=len(queries),
        )

    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
