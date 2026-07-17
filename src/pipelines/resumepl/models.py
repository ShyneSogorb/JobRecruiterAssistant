from pydantic import BaseModel

from modules.models.job_models import JobOffer
from modules.models.candidate_models import CandidateProfile


class ResumePipelineResult(BaseModel):
    job: JobOffer
    resume: CandidateProfile
