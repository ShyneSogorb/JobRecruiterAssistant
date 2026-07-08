from pydantic import BaseModel

from src.jobs.models import JobOffer
from src.candidate.models import CandidateProfile


class ResumePipelineResult(BaseModel):
    job: JobOffer
    resume: CandidateProfile
