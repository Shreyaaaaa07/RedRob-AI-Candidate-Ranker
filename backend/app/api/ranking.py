from fastapi import APIRouter
from app.services.ranking_service import RankingService

router = APIRouter(
    prefix="/rankings",
    tags=["Rankings"]
)

ranking_service = RankingService()


@router.get("/")
def get_rankings():
    return ranking_service.get_rankings()