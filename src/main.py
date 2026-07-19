from modules.database.db_client import DbJobClient
from modules.models.job_models import EJobState
import src.utils.utils_library as Utils
from src.utils.logger import Logger
from modules.ui.ui import WindowObject

from .job_worker import get_worker_thread, stop_event

@Utils.TimedFunction
def main():

    worker = get_worker_thread()
    worker.start()
    window = WindowObject(DbJobClient())

    window.run()
    
    if worker.is_alive():
        logger.log("Exiting while generating cvs, safely cancelling task...")
        stop_event.set()
        worker.join()
        logger.log("CV maker thread successfully ended or canceled")

    logger.log("Exiting")

        

if __name__ == "__main__":
    logger = Logger.create_global("Main")
    main()
