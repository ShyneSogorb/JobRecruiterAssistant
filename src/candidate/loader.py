import json
from pathlib import Path


class CandidateLoader:

    # @staticmethod
    # def load(path: str | Path) -> CandidateProfile:
    #     with open(path, "r", encoding="utf-8") as file:
    #         data = json.load(file)

    #     return CandidateProfile.model_validate(data)

    @staticmethod
    def load(path: str | Path) -> str:
        with open(path, "r", encoding="utf-8") as file:
            return file.read()
