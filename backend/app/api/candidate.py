from fastapi import APIRouter, HTTPException
from app.services.candidate_service import CandidateService

router = APIRouter(
    prefix="/candidate",
    tags=["Candidate"]
)

candidate_service = CandidateService()


@router.get("/{candidate_id}")
def get_candidate(candidate_id: str):

    candidate = candidate_service.get_candidate(candidate_id)

    if candidate is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    return candidate