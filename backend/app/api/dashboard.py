from fastapi import APIRouter
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

dashboard_service = DashboardService()


@router.get("/")
def get_dashboard():

    return dashboard_service.get_dashboard_stats()