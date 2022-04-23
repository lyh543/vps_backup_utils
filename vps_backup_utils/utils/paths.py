import os
from pathlib import Path
import pipes
from typing import Union

PathOrStr = Union[Path, str]


def to_path(path: PathOrStr, expanduser=True) -> Path:
    if type(path) == str:
        if expanduser:
            path = os.path.expanduser(path)
        return Path(path)
    else:
        if expanduser:
            path = path.expanduser()
        return path


def quote_path(path: Path, append_slash = False) -> str:
    if append_slash:
        path_str = str(path / '@')[0:-1]
    else:
        path_str = str(path)
    return pipes.quote(path_str)
