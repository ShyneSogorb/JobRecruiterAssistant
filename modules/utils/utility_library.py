from pathlib import Path
import re


def symbols_removal(string: str) -> Path:
    return Path(re.sub(r"[\\\s\(\)\|\-\,]", "_", string))
