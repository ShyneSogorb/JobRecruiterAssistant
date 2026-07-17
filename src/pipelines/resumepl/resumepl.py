from src.candidate.loader import CandidateLoader
from modules.models.candidate_models import CandidateProfile
from src.utils.logger import Logger
from modules.models.job_models import JobOffer

from src.cv.adapter import CVAdapter
from modules.job.parser import JobOfferParser
from src.pipelines.resumepl.models import ResumePipelineResult
from pathlib import Path

from pydantic import BaseModel

from modules.models.job_models import JobOffer
from modules.models.candidate_models import CandidateProfile


class ResumePipeline:

    @property
    def candidate(self) -> str:
        return self.profile

    #def __init__(self, parser: JobOfferParser, adapter: CVAdapter, logger: Logger, profile: CandidateProfile):
    def __init__(self, parser: JobOfferParser, adapter: CVAdapter, logger: Logger, profile: str):
        self.parser = parser
        self.adapter = adapter
        self.logger = logger
        self.profile = profile

    def run( self, offer: str) -> ResumePipelineResult:

        
        #self.logger.save_json("Candidate Master CV", self.profile)

        self.logger.log("Parsing offer...")
        job = self.parser.parse(offer)
        self.logger.log("Offer successfully parsed")
        self.logger.save_json(f"parsed_{job.company}", job)

        self.logger.log("Adapting CV...")
        adapted = self.adapter.adapt(self.profile, job)
        self.logger.log(f"CV adapted for position {job.company}")

        self.logger.save_json(f"CV_{job.company}", adapted)

        return ResumePipelineResult(job=job, resume=adapted)