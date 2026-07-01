from fastapi import APIRouter
from pydantic import BaseModel
from app.services.job_description_service import JobDescriptionService

router = APIRouter(
    prefix="/job-description",
    tags=["Job Description"]
)


class JobDescriptionRequest(BaseModel):
    text: str


@router.post("/")
def upload_job_description(request: JobDescriptionRequest):
    """
    Temporary endpoint for frontend integration.
    Later this will call the JD parser.
    """

    service = JobDescriptionService()

    parsed = service.parse(request.text)

    return {

        "status": "success",

        "message": "Job Description Parsed",

        "parsed_signals": parsed

    }


@router.get("/parsed")
def get_parsed_job_description():
    return {
        "skills": [
            "Python",
            "Machine Learning",
            "LLMs",
            "Vector Database"
        ],
        "experience": "5+ years",
        "education": "Bachelor's Degree"
    }