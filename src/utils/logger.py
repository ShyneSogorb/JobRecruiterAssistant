import json
import os
import textwrap
from typing import Any
from pydantic import BaseModel
import datetime
import re

def _wrap_strings(obj: Any, width: int) -> Any:
    if isinstance(obj, BaseModel):
        obj = obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()

    if isinstance(obj, dict):
        return {
            key: _wrap_strings(value, width)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            _wrap_strings(value, width)
            for value in obj
        ]

    if isinstance(obj, str):
        stripped = obj.strip()

        # Si la cadena parece contener JSON, devolvemos el objeto YA PARSEADO
        # (no un string re-serializado), para que el json.dumps exterior lo
        # trate como estructura nativa y no como texto escapado.
        if stripped.startswith(("{", "[")):
            try:
                parsed = json.loads(stripped)
                return _wrap_strings(parsed, width)
            except json.JSONDecodeError:
                pass

        return textwrap.fill(obj, width=width)

    return obj


def format_log(data: Any, width: int = 100) -> str:
    if isinstance(data, BaseModel):
        data = data.model_dump() if hasattr(data, "model_dump") else data.dict()

    if isinstance(data, (dict, list)):
        return json.dumps(
            _wrap_strings(data, width),
            indent=2,
            ensure_ascii=False,
        )

    if isinstance(data, str):
        stripped = data.strip()

        if stripped.startswith(("{", "[")):
            try:
                parsed = json.loads(stripped)

                return json.dumps(
                    _wrap_strings(parsed, width),
                    indent=2,
                    ensure_ascii=False,
                )
            except json.JSONDecodeError:
                pass

        return textwrap.fill(data, width=width)

    return textwrap.fill(str(data), width=width)


class Logger:

    static_logger: "Logger"

    @property
    def _get_time(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _get_day(self):
        return datetime.date.today()

    def log(self, text: str):
        print(text)
        self.save(text)

    def __init__(self, task: str):
        self.root = f"logs/{re.sub(r'[\\s:.-]', '_', self._get_time)}/{task}/"
        os.makedirs(os.path.dirname(self.root), exist_ok=True)

    @classmethod
    def create_global(cls, task: str) -> "Logger":
        logger = cls(task)
        cls.static_logger = logger
        return logger

    @classmethod
    def get_global(cls) -> "Logger":
        return cls.static_logger

    def save(self, data: Any, filename: str = "log", format: str = "log"):
        timestamp = f"[{self._get_time}]: " if format == "log" else ""

        text = format_log(data).replace("\\n", "\n")
        lines = text.split("\n")

        with open(f"{self.root}/{filename}.{format}", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}{text}\n")
            for l in lines:
                timestamp = ""