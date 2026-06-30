from fastapi import APIRouter, HTTPException
from app.services.explainability_service import ExplainabilityService

router = APIRouter(
    prefix="/explainability",
    tags=["Explainability"]
)

service = ExplainabilityService()


@router.get("/{candidate_id}")
def get_candidate_explainability(candidate_id: str):
    result = service.get_candidate_evidence(candidate_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return result