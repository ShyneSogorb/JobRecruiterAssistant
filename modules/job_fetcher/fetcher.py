from datetime import date, datetime, timedelta

from jobspy import scrape_jobs, Site
import pandas as pd
import src.utils.utils_library as Utils
import os

import modules.utils.assetloader as AssetLoader
from database.settingsschema import ScrappleJobQuerySchema

from modules.job_fetcher.job_cache import JobCache

DATABASE_PATH="database\\jobs"
DATETIME_FORMAT='%Y-%m-%d %H'


class JobFetcher:

    def __init__(self, logger) -> None:
        self.logger = logger

    @classmethod
    def _get_last_update(cls, db: str) -> datetime | None:
        path = os.path.join(DATABASE_PATH, db, "last_update.info")
        if not os.path.exists(path): 
            return None
        
        with open(path) as f:
            return datetime.strptime(f.read(), DATETIME_FORMAT)
        
    @classmethod
    def _set_last_update(cls, now: datetime, db: str):
        path = os.path.join(DATABASE_PATH, db, "last_update.info")
        
        with open(path, "w", encoding="utf-8") as f:
            return f.write(now.strftime(DATETIME_FORMAT))
        
    @classmethod
    def _get_databases(cls):
        dbs = list(map(lambda i: os.path.join(DATABASE_PATH, i), os.listdir(DATABASE_PATH)))
        dbs = list(filter(lambda i: os.path.isdir(i) and "pycache" not in i, dbs))
        dbs = list(map(lambda i: os.path.basename(i), dbs))
        return dbs
    
    @classmethod
    def _build_path(cls, database):
        return f"jobs_raw/{database}/jobs.csv"

    @Utils.TimedFunction
    def fetch_jobs(self) -> list[pd.DataFrame]:
        cache = JobCache(self.logger)
        jobs: list[pd.DataFrame] = []
    
        dbs = self._get_databases()
        now = datetime.now()
    
        for db in dbs:
            cache_path = self._build_path(db)
            self.logger.log(f"Fetching for database {db}")

            db_settings = os.path.join(DATABASE_PATH, db, "settings.py")
            _last_update = self._get_last_update(db)
            if not _last_update == None:
                last_update: datetime = _last_update
                if (now - last_update) < timedelta(days=1):
                    load = cache.load(cache_path)
                    jobs.append(cache.cast(load))
                    continue

            query: ScrappleJobQuerySchema = AssetLoader.load_module(db_settings)

            jobs_fetched = query.fetch()

            if jobs_fetched.empty: 
                print("No jobs found")
                continue
    
            jobs.append(jobs_fetched)
            cache.save(jobs_fetched, cache_path)
            self._set_last_update(now, db)
        
        return [job for job in jobs if job is not None]
    
    def clear_cache(self):
        self.logger.log("Clear")
        cache = JobCache(self.logger)
        for db in self._get_databases():
            cache._clear_cache(self._build_path(db))