import os
from typing import TypeAlias, Optional
from dataclasses import dataclass, asdict


FileName: TypeAlias = str | bytes | os.PathLike


@dataclass
class FileOptions:
    """Options as they can be used for opening a file. See Python function *open*."""

    encoding: Optional[str] = None
    errors: Optional[str] = None
    newline: Optional[str] = None


file_options = FileOptions(None, None, None)
""" Options used for reading and writing files. See Python function *open*. """


def read_file(in_file_name: FileName) -> str:
    """Load text from *in_file_name* with universal newline mode enabled."""
    # Newline is None (the default) -> universal newlines mode is enabled.
    # Lines in the input can end in '\n', '\r', or '\r\n', and these are
    # translated into '\n' before being returned to the caller.
    with open(in_file_name, **asdict(file_options)) as f_in:
        s_in = f_in.read()
    return s_in


def write_file(out_file_name: FileName, content: str) -> None:
    """Load text from *in_file_name* with universal newline mode enabled."""
    with open(out_file_name, "w", **asdict(file_options)) as f_out:
        f_out.write(content)
