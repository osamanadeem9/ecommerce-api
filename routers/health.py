from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    """API health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow()}
