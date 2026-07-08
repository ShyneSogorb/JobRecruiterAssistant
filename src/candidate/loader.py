import json
from pathlib import Path

from src.candidate.models import CandidateProfile

class CandidateLoader:

    @staticmethod
    def load(path: str | Path) -> CandidateProfile:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return CandidateProfile.model_validate(data)