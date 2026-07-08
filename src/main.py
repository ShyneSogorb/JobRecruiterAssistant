from src.cv.adapter import CVAdapter
from src.ai.prompts import PromptBuilder
from src.jobs.parser import JobOfferParser
from src.ai.client import AIClient
from src.candidate.loader import CandidateLoader
from src.utils.logger import Logger
from src.pipelines.resumepl.resumepl import ResumePipeline

def main():

    logger = Logger("Main")

    logger.log("Creating AI client")
    ai = AIClient()
    logger.log("Ai client created")

    logger.log("Creating prompt builder")
    prompts = PromptBuilder()
    logger.log("Prompt builder created")

    logger.log("Creating job offer parser")
    parser = JobOfferParser(ai, prompts)
    logger.log("Job parser created")

    logger.log("Creating a cv adapter")
    adapter = CVAdapter(ai, prompts)
    logger.log("CV adapter created")


    logger.log("Loading candidate master json")
    candidate = CandidateLoader.load("src/profile/MasterCV.json")
    logger.log(f"Candidate {candidate.personal.name} data successfully loaded")

    resume_pipeline = ResumePipeline(parser, adapter, Logger("Resume pipeline"), candidate)

    logger.log("Reading job info")
    with open("test/job.txt", encoding="utf8") as f:
        offer = f.read()
    logger.log("Job info successfully readed")

    resume_result = resume_pipeline.run(offer)

if __name__ == "__main__":
    main()