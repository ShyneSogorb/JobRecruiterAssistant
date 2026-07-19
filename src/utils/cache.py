from pathlib import Path
from os import listdir, remove, removedirs
from os.path import isfile, join

import re
from typing import Any, Callable

def _default_save_method(target: Path, data: Any) -> None:
    with open(target, "w", encoding="utf8") as f: 
        f.write(data)

def _default_load_method(target: Path) -> str:
    with open(target, "r", encoding="utf8") as f: 
        return f.read()


class CacheManager:

    def _fix_cache_path(self, string: str) -> Path:
        string = "cache/" + string
        return Path(re.sub(r"[\s\(\)\|\-]", "_", string))
    
    def _get_default_save_method(self) : 
        return _default_save_method
    
    def _get_default_load_method(self) :
        return _default_load_method
    
    def __init__(self, logger) -> None:
        self.logger = logger

    def save(
        self,
        data: Any,
        path: str | Path,
        save_method: Callable[[Path, Any], None] | None = None
    ) -> None:
        
        save_method = self._get_default_save_method() if save_method == None else save_method

        path = self._fix_cache_path(str(path))
        Path(path).parent.mkdir(parents=True, exist_ok=True)

        self.logger.log(f"Saving {path.name} at {str(path)} by {save_method} method")
        save_method(path, data)

    def load(
        self,
        path: str | Path,
        load_method: Callable[[Path], Any] | None = None
    ):
        
        load_method = self._get_default_load_method() if load_method == None else load_method

        path = self._fix_cache_path(str(path))

        self.logger.log(f"Trying to load {path.name} at {str(path)} by {load_method} method")
        if not path.exists(): 
            self.logger.log(f"{path.name} could not be loaded because {path} does not exist")
            return None

        self.logger.log(f"{path.name} loaded at {str(path)} by {load_method} method")
        return load_method(path)
    
    def _clear_cache(self, path: str | Path):
        
        path = self._fix_cache_path(str(path))
        if path.exists(): 
            remove(path)
            removedirs(path.parent)
            self.logger.log(f"Cache cleared at {path}")
            return
        
        self.logger.log(f"{path} does not exist, can not clear")

        if path.parent.exists():
            removedirs(path.parent)

