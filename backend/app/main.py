from fastapi import FastAPI
from app.api.dashboard import router as dashboard_router
from app.api.ranking import router as ranking_router
from app.api.candidate import router as candidate_router
from app.api.rank import router as rank_router

app = FastAPI(
    title="Redrob AI Candidate Ranker API",
    version="1.0.0"
)

# Register Routers
app.include_router(dashboard_router)
app.include_router(ranking_router)
app.include_router(candidate_router)
app.include_router(rank_router)



@app.get("/")
def root():
    return {
        "message": "Redrob AI Candidate Ranker Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }