from typing import Optional, Any
import importlib.util
import os

def _get_module_name(filename: str) -> str:
    name, _ = os.path.splitext(os.path.basename(filename))
    return name

def import_file(filename: str, name: Optional[str] = None) -> Any:
    module_name = name or _get_module_name(filename)

    spec = importlib.util.spec_from_file_location(module_name, filename)
    loaded_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded_mod)

    return loaded_mod
