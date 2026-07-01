from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.ranking import router as ranking_router
from app.api.candidate import router as candidate_router
from app.api.rank import router as rank_router
from app.api.job_description import router as job_description_router
from app.api.explainability import router as explainability_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="Redrob AI Candidate Ranker API",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://red-rob-ai-candidate-ranker.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Routers
# -----------------------------
app.include_router(dashboard_router)
app.include_router(ranking_router)
app.include_router(candidate_router)
app.include_router(rank_router)
app.include_router(job_description_router)
app.include_router(explainability_router)
app.include_router(analytics_router)


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