from src.candidate.loader import CandidateLoader
from src.candidate.models import CandidateProfile
from src.utils.logger import Logger

from src.cv.adapter import CVAdapter
from src.jobs.parser import JobOfferParser
from src.pipelines.resumepl.models import ResumePipelineResult
from pathlib import Path


class ResumePipeline:

    @property
    def candidate(self) -> CandidateProfile:
        return self.profile

    def __init__(self, parser: JobOfferParser, adapter: CVAdapter, logger: Logger, profile: CandidateProfile):
        self.parser = parser
        self.adapter = adapter
        self.logger = logger
        self.profile = profile

    def run( self, offer: str) -> ResumePipelineResult:

        
        self.logger.save_json("Candidate Master CV", self.profile)

        self.logger.log("Parsing offer...")
        job = self.parser.parse(offer)
        self.logger.log("Offer successfully parsed")
        self.logger.save_json("parsed_job", job)

        self.logger.log("Adapting CV...")
        adapted = self.adapter.adapt(self.profile, job)
        self.logger.log(f"CV adapted for position {job.company}")

        self.logger.save_json("adapted_resume", adapted)

        return ResumePipelineResult(job=job, resume=adapted)