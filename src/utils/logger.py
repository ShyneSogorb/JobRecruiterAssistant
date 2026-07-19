import os
from threading import RLock
from typing import Any
import datetime
import re

from src.utils.sync_library import synchronized_class

@synchronized_class
class Logger:

    static_logger: dict[str, "Logger"] = {}

    @property
    def _get_time(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _get_day(self):
        return datetime.date.today()

    def log(self, text: str):
        print(text)
        self.save(text)

    def __init__(self, task: str):
        self._lock = RLock()
        self.root = f"logs/{re.sub(r'[\\s:.-]', '_', self._get_time)}/{task}/"
        os.makedirs(os.path.dirname(self.root), exist_ok=True)

    @classmethod
    def create_global(cls, task: str) -> "Logger":
        logger = cls(task)
        cls.static_logger[task] = logger
        return logger

    @classmethod
    def get_global(cls, task:str|None = None) -> "Logger":
        if task is None:
            return list(cls.static_logger.values())[0]
        return cls.static_logger[task]

    def save(self, data: Any, filename: str = "log", format: str = "log"):
        timestamp = f"[{self._get_time}]: " if format == "log" else ""

        text = data.replace("\\n", "\n")
        lines = text.split("\n")

        with open(f"{self.root}/{filename}.{format}", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}{text}\n")
            for l in lines:
                timestamp = ""