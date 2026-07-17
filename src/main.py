import json
import re

import src.utils.utils_library as Utils
import pandas as pd
from modules.job_fetcher.models import JobSpyParser
from modules.models.candidate_models import Skill
from modules.models.job_models import JobOffer
from src.cv.adapter import CVAdapter
from src.ai.prompts import PromptBuilder
from modules.job.parser import JobOfferParser
from src.ai.client import AIClient
from src.utils.logger import Logger
from src.utils.cache import CacheManager
from src.pipelines.resumepl.resumepl import ResumePipeline
from modules.job_fetcher.fetcher import JobFetcher
from modules.job_fetcher.job_cache import JobCache
from src.jobs.aplication.html_maker import HtmlCVMaker
from os import listdir
import os
from os.path import isfile, join
from pathlib import Path
from modules.database.db_client import DbJobClient
from src.aplication_pipeline import ApplicationPipeline
from modules.candidate_maker.candidatemaker import CandidateMakerPipeline
from modules.job_fetcher.fetcher import JobFetcher


from weasyprint import HTML

@Utils.TimedFunction
def main():

    

    logger = Logger.create_global("Main")

    #jobs = _get_jobs(logger)

    fetcher = JobFetcher()

    jobs_dict = fetcher.fetch_jobs(logger)

    logger.log("Creating AI client")
    ai = AIClient(logger)
    logger.log("Ai client created")

    logger.log("Creating job offer parser")
    parser = JobOfferParser(ai)
    logger.log("Job parser created")
    
    cache = CacheManager(logger)

    all_jobs: dict[str, list[JobOffer]] = {}

    database = DbJobClient()

    # logger.log(f"Parsing {} jobs")
    # for db, jobs in jobs_dict.items():
    #     if jobs.empty: continue
    #     all_jobs[db] = JobSpyParser.parse(jobs)

    #     cache.save("\n".join(map(lambda job: job.model_dump_json() , all_jobs[db])), "test.json")
    #     cache.save(json.dumps(JobOffer.model_json_schema(), indent=4), "schema.json")

    # logger.log("IA job parsing")
    # for db, jobs in all_jobs.items():
    #     logger.log(f"Parsing jobs as {db}")
    #     for job in jobs:
    #         if (
    #             database.applied_contains_job(db, job.id)
    #             or database.pending_contains_job(db, job.id)
    #             or database.ready_contains_job(db, job.id)
    #             ): continue

    #         offer = parser.parse(job).model_dump_json()
    #         database.insert_new_job(db, offer)

    def _not_in_database(job: JobOffer) -> bool:
        return not (
            database.ready_contains_job(db, job.id)
            or database.applied_contains_job(db, job.id)
            or database.pending_contains_job(db, job.id)
        )

    num = len(jobs_dict)
    logger.log(f"Parsing {num} jobs chunk")
    for n, (db, jobs) in enumerate(jobs_dict.items(), start=1):
        if jobs.empty: continue
        logger.log(f"{n}/{num}")
        jobs = all_jobs[db] = list(filter(_not_in_database, JobSpyParser.parse(jobs)))

        for job in jobs:
            database.insert_raw_job(db, job.model_dump_json())

    all_jobs: dict[str, list[JobOffer]] = {}
    for table in database._get_all_job_tables():
        all_jobs[table] = database.get_all_pending_jobs_at_table_as(table, JobOffer)


    logger.log("IA job parsing")
    for db, jobs in all_jobs.items():
        logger.log(f"Parsing jobs as {db}")
        num = len(jobs)
        for n, job in enumerate(jobs, start=0):

            if database.ready_contains_job(db, job.id): 
                continue

            logger.log(f"{n}/{num}")
            offer = parser.parse(job).model_dump_json()
            database.remove_raw_job(db, offer)
            database.insert_new_job(db, offer)


    logger.log("Creating prompt builder")
    prompts = PromptBuilder()
    logger.log("Prompt builder created")

    logger.log("Creating a cv adapter")
    adapter = CVAdapter(ai, prompts)
    logger.log("CV adapter created")

    logger.log("Creating html generator")
    html_generator = HtmlCVMaker(ai, prompts)
    logger.log("Html generator created")

    app = ApplicationPipeline(ai, CacheManager(logger), logger)

    for db, _jobs in database.get_all_pending_jobs().items():
        num = len(_jobs)
        for n, _job in enumerate(_jobs, start=1):
            job = JobOffer.model_validate_json(_job)

            logger.log(f"{n}/{num}")
            cv_path = app.run(job)

            database.add_cv_link(cv_path, job.id, db)

    # for db, _jobs in database.get_all_pending_jobs().items():
    #     for _job in _jobs:
    #         job = JobOffer.model_validate_json(_job)

    #         cv_path = app.run(job)

    #         database.add_cv_link(cv_path, job.id, db)
        

if __name__ == "__main__":
    logger = Logger.create_global("Main")
    main()
