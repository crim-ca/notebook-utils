import argparse
import logging
import nbformat
import os
import pathlib
import shlex
import sys
import typing

PathLike = typing.TypeVar("PathLike", str, pathlib.Path)

_logger = logging.getLogger(__name__)


def strip_to_stdout(notebook_path: PathLike):
    quoted_path = shlex.quote(str(notebook_path))
    return f"jupyter nbconvert --to notebook --ClearOutputPreprocessor.enabled=True --stdout {quoted_path} 2>/dev/null"


def notebook_to_html(notebook_path: PathLike, documentation_path: PathLike="."):
    os.system(f"jupyter nbconvert --output-dir='{documentation_path}' --to html " + notebook_path)


def notebook_is_stripped(notebook_path: PathLike):
    notebook = nbformat.read(notebook_path, nbformat.NO_CONVERT)
    for cell in notebook.cells:
        if cell.cell_type == "code":
            if len(cell.outputs) != 0:
                return False
    return True


def notebooks_are_stripped_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dir",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    args = parser.parse_args()

    are_stripped = []
    for notebook_file in args.dir.rglob("*.ipynb"):
        if notebook_file.parent.stem != ".ipynb_checkpoints":
            _logger.info(f"Checking {notebook_file}...")
            if notebook_is_stripped(notebook_file):
                are_stripped.append(True)
            else:
                are_stripped.append(False)
                _logger.error(f"Notebook file {notebook_file} is not stripped.")

    sys.exit(not all(are_stripped))
