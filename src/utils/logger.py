import os

from pydantic import BaseModel
import datetime
import re

class Logger:

    @property
    def _get_time(self) -> str: 
        return datetime.datetime.now().strftime(("%Y-%m-%d_%H-%M-%S"))
    
    def _get_day(self):
        return datetime.date.today()
    
    def log(self, text:str):
        print(text)
        self.save_text("log", text)

    def __init__(self, task: str):
        self.root = f"logs/{re.sub(r"[\s:.-]", "_", self._get_time)}/{task}/"
        os.makedirs(os.path.dirname(self.root), exist_ok=True)

    def save_prompt(self, prompt: str):
        self.save_text("conversation", prompt)

    def save_response(self, response: str):
        self.save_text("conversation", response)

    def save_json(self, filename: str, obj: BaseModel):
        self.save_text(filename, obj.model_dump_json(indent=4), "json")

    def save_text(self, filename: str, text: str, format:str ="log"):
        timestamp = f"[{self._get_time}]: " if format == "log" else ""

        with open(f"{self.root}/{filename}.{format}", "a+", encoding="utf-8") as f:
            f.write(f"{timestamp}{text}\n")
