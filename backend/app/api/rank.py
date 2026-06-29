from fastapi import APIRouter, HTTPException
from app.services.rank_service import RankService

router = APIRouter(
    prefix="/rank",
    tags=["Ranking Pipeline"]
)

rank_service = RankService()


@router.post("/")
def run_ranking():

    try:

        result = rank_service.run_pipeline()

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )