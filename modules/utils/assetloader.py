import importlib.util
from pathlib import Path
import sys
from typing import Any

def load_module(path) -> Any:
    spec = importlib.util.spec_from_file_location("dynamic_module", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"No se pudo cargar {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    load = getattr(module, "load", None)
    if not callable(load):
        raise TypeError(f"{path} debe definir una función load()")

    
    return module.load()
    