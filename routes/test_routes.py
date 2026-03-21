from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field, model_validator

from core.test_generator import generate_test

router = APIRouter(prefix="/test", tags=["Test"])


class JobPostingTestRequest(BaseModel):
    """
    Job posting document (e.g. from Mongo). Unknown fields (_id, createdAt, …) are ignored.
    Optional `difficulty` can be sent alongside the job fields.
    """

    model_config = ConfigDict(extra="ignore")

    title: Optional[str] = None
    description: str = ""
    skillsRequired: list[str] = Field(default_factory=list)
    difficulty: str = "Intermediate"
    experienceRequired: Optional[float] = None
    profile: Optional[str] = None
    jobType: Optional[str] = None
    salaryRange: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def drop_mongo_dollar_keys(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if not str(k).startswith("$")}
        return data


def _build_job_description(job: JobPostingTestRequest) -> str:
    parts: list[str] = []
    if job.title:
        parts.append(f"Title: {job.title}")
    if job.profile:
        parts.append(f"Role profile: {job.profile}")
    if job.description:
        parts.append(job.description)
    if job.experienceRequired is not None:
        parts.append(f"Minimum experience (years): {job.experienceRequired}")
    if job.jobType:
        parts.append(f"Job type: {job.jobType}")
    if job.salaryRange:
        parts.append(f"Salary range: {job.salaryRange}")
    return "\n\n".join(parts) if parts else job.description


@router.post("/generate")
def generate(req: JobPostingTestRequest):
    job_desc = _build_job_description(req)
    return generate_test(req.skillsRequired, job_desc, req.difficulty)
