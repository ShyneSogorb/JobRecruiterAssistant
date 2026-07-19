import threading

import src.utils.utils_library as Utils
from modules.job_fetcher.models import JobSpyParser
from modules.models.job_models import EJobState, JobApplication, JobOffer
from modules.job.parser import JobOfferParser
from src.ai.client import AIClient
from src.utils.logger import Logger
from src.utils.cache import CacheManager
from modules.job_fetcher.fetcher import JobFetcher
from modules.database.db_client import DbJobClient
from src.aplication_pipeline import ApplicationPipeline
from modules.job_fetcher.fetcher import JobFetcher


from weasyprint import HTML

stop_event = threading.Event()

def get_worker_thread():
    return threading.Thread(
        target=_internal_work_loop,
        args=(stop_event,)
    )


def _internal_work_loop(stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            _internal_work(stop_event)
        except:
            Logger.get_global().log(f"Exception during cv generation. {"Expected during cancelation, ignore" if stop_event.is_set() else "Unexpected error"}")
            if not stop_event.is_set():
                raise
                
        

@Utils.TimedFunction
def _internal_work(stop_event: threading.Event):

    logger = Logger.get_global("Main")

    fetcher = JobFetcher(logger)

    

    jobs_fetched = fetcher.fetch_jobs()

    logger.log("Creating AI client")
    ai = AIClient(stop_event, logger)
    logger.log("Ai client created")

    logger.log("Creating job offer parser")
    parser = JobOfferParser(ai)
    logger.log("Job parser created")
    
    database = DbJobClient()

    num = len(jobs_fetched)
    logger.log(f"Parsing {num} jobs chunk")
    for n, jobs_fd in enumerate(jobs_fetched, start=1):
        
        if stop_event.is_set():
            logger.log("Stopping working thread...")
            return
        
        if jobs_fd.empty: continue

        logger.log(f"{n}/{num}")
        jobs = [ job for job in JobSpyParser.parse(jobs_fd)]

        for job in jobs:
            database.insert(JobApplication(id=job.id, job=job, state=EJobState.RAW))

    logger.log("RAW jobs saved")
    fetcher.clear_cache()

    logger.log("IA job parsing")
    raw_jobs = database.get_all_jobs_by_state(EJobState.RAW)

    num = len(raw_jobs)
    for n, job in enumerate(raw_jobs, start=1):

        if stop_event.is_set():
            logger.log("Stopping working thread...")
            return

        logger.log(f"{n}/{num}")
        job.job = parser.parse(job.job)
        job.state = EJobState.PARSED
        database.update_job(job)

    app = ApplicationPipeline(ai, CacheManager(logger), logger)

    parsed_jobs = database.get_all_jobs_by_state(EJobState.PARSED)
    num = len(parsed_jobs)
    for n, job in enumerate(parsed_jobs, start=1):

        if stop_event.is_set():
            logger.log("Stopping working thread...")
            return

        job = app.run(job)
        database.update_job(job)
        

        logger.log(f"{n}/{num}")

    logger.log("Worker finished")

