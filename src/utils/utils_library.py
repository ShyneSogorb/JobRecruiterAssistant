from src.candidate.loader import CandidateLoader
from time import perf_counter
from functools import wraps
from src.utils.logger import Logger
import traceback

def get_candidate():
    return CandidateLoader.load("src/profile/aboutme.md")

def TimedFunction(func):

    def _get_time_str(total_time):
        if total_time < 60:
            time_str = f"{total_time:.2f} seconds"
        else:
            total_seconds = int(round(total_time))
            minutes, seconds = divmod(total_seconds, 60)

            minute_text = "minute" if minutes == 1 else "minutes"
            second_text = "second" if seconds == 1 else "seconds"

            time_str = (
                f"{minutes} {minute_text} and "
                f"{seconds} {second_text} ({total_seconds}s)"
            )


    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = Logger.get_global()
        start = perf_counter()

        try:
            return func(*args, **kwargs)
        except Exception as e:
            total_time = perf_counter() - start
            logger.log(f"{func.__name__} failed at {_get_time_str(total_time)}")
            logger.log(traceback.format_exc())
            raise
        finally:
            total_time = perf_counter() - start
            logger.log(f"{func.__name__} took {_get_time_str(total_time)}")

    return wrapper
