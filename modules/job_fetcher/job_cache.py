from pathlib import Path
from typing import Any
from src.utils.cache import CacheManager

import pandas as pd
import re

def _save_csv(target: Path, data: pd.DataFrame) -> None:
    data.to_csv(target, index=False)

def _load_csv(target: Path) -> pd.DataFrame:
    return pd.read_csv(target)



class JobCache(CacheManager):

    def _symbols_removal(self, string: str) -> Path:
        return Path(re.sub(r"[\s\(\)\|\-]", "_", string))

    def _get_default_save_method(self) : 
        return _save_csv
    
    def _get_default_load_method(self) : # type: ignore
        return _load_csv
    
    def cast(self, source: Any) -> pd.DataFrame:
        return source
