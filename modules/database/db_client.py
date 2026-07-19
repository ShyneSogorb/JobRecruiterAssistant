import sqlite3
from functools import wraps
from src.utils.logger import Logger
from threading import RLock

from modules.models.job_models import EJobState, JobApplication, JobOffer, Salary
from src.utils.sync_library import synchronized_class

EMPTY_LINE = r"^\s*$"

TABLE = "job_applications"

ID = "id"
JOB = "job"
CV = "cv"
CV_PATH = "cv_path"
HIRING_MANAGER = "hiring_manager"
COVER_LETTER = "cover_letter"
STATE = "state"
SALARY="salary"
SCORE="score"

ALL_FIELDS = [
    ID,
    JOB,
    CV,
    CV_PATH,
    HIRING_MANAGER,
    COVER_LETTER,
    STATE,
    SALARY,
    SCORE
]

def _get_fields(excluded: list[str] | None = None):
    excluded = excluded or []
    return [field for field in ALL_FIELDS if field not in excluded]
    

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE} (
    {ID} TEXT PRIMARY KEY,
    {JOB} TEXT NOT NULL,
    {CV} TEXT,
    {CV_PATH} TEXT,
    {HIRING_MANAGER} TEXT,
    {COVER_LETTER} TEXT,
    {STATE} TEXT NOT NULL,
    {SALARY} TEXT,
    {SCORE} REAL
)"""

V1 = [
    f"ALTER TABLE {TABLE} ADD COLUMN {SALARY} TEXT",
    f"ALTER TABLE {TABLE} ADD COLUMN {SCORE} REAL"
]

VERSIONS = [V1]

    
def AutoCommit(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        value = func(self, *args, **kwargs)
        self.commit()
        return value

    return wrapper



@synchronized_class
class DbJobClient():

    def __init__(self) -> None:
        self._lock = RLock()
        self.con = sqlite3.connect("Jobs.db")
        self.logger = Logger.get_global()

        self.con.row_factory = sqlite3.Row
        self.con.set_trace_callback(self.logger.log)
        version = self.con.execute("PRAGMA user_version").fetchone()[0]
        print(f"Connected to{version}")

        with self.con:
            for i, migration in enumerate(VERSIONS, start=1):
                if version < i:
                    for statement in migration:
                        self.con.execute(statement)
                self.con.execute(f"PRAGMA user_version = {i}")

        self.con.execute(CREATE_TABLE)

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

        
    @classmethod
    def _row_to_application(cls, row) -> JobApplication:
        return JobApplication(
            id=row[ID],
            job=JobOffer.model_validate_json(row[JOB]),
            cv=row[CV],
            cv_path=row[CV_PATH],
            hiring_manager=row[HIRING_MANAGER],
            cover_letter=row[COVER_LETTER],
            state=EJobState(row[STATE]),
            salary=Salary.model_validate_json(row[SALARY]) if row[SALARY] is not None else None,
            score=row[SCORE]
        )

    @classmethod
    def _tuple_insert(cls, app: JobApplication) -> tuple:
        return (app.id, app.job.model_dump_json(), app.cv, app.cv_path, app.hiring_manager, app.cover_letter, app.state.value, app.salary.model_dump_json() if app.salary is not None else None, app.score)
    
    @classmethod
    def _tuple_update(cls, app: JobApplication) -> tuple:
        return (app.job.model_dump_json(), app.cv, app.cv_path, app.hiring_manager, app.cover_letter, app.state.value, app.salary.model_dump_json() if app.salary is not None else None, app.score, app.id)

    @AutoCommit
    def insert(self, app: JobApplication):
        try:
            self.con.execute(f"""INSERT INTO {TABLE} ({", ".join(_get_fields())})
        VALUES ({"?, ".join(["" for _ in _get_fields()])}?)""",
                self._tuple_insert(app)
            )
        except sqlite3.IntegrityError:
            self.logger.log(f"Tried to insert {app.id}({app.job.company}) which already exists")


    def get_by_id(self, id: str) -> JobApplication | None:
        
        row = self.con.execute(
            f"SELECT * FROM {TABLE} WHERE {ID}=?",
            (id,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_application(row)

    def get_all_jobs_by_state(self, state: EJobState) -> list[JobApplication]:

        result = self.con.execute(
            f"SELECT * FROM {TABLE} WHERE {STATE}=?",
            (state.value,)
        ).fetchall()
        return [self._row_to_application(row) for row in result]
    
    def get_num_ready_jobs(self) -> int:
        row = self.con.execute(
            f"SELECT COUNT(DISTINCT id) FROM {TABLE} WHERE {STATE}=?",
            (EJobState.READY.value,)
        ).fetchone()
        return row[0]
    
    def get_ready_job(self, offset: int) -> JobApplication:
        row = self.con.execute(
            f"SELECT * FROM {TABLE} WHERE {STATE}=? LIMIT 1 OFFSET ?",
            (EJobState.READY.value, offset)
        ).fetchone()
        return self._row_to_application(row)

    @AutoCommit
    def delete(self, id:str) -> None:
        self.con.execute(f"DELETE FROM {TABLE} WHERE {ID}=?", (id,))

    @AutoCommit
    def set_job_state(self, id:str, new_state: EJobState) -> None:
        self.con.execute(f"UPDATE {TABLE} SET {STATE}=? WHERE {ID}=?", (new_state.value, id,))
    
    @AutoCommit
    def update_job(self, job: JobApplication):
        assignments = ", ".join(
            f"{field}=?"
            for field in _get_fields([ID])
        )

        self.con.execute(f"UPDATE {TABLE} SET {assignments} WHERE {ID}=?", self._tuple_update(job))
