import argparse
import logging
import nbformat
import os
import pathlib
import sys
import typing

PathLike = typing.TypeVar("PathLike", str, pathlib.Path)

_logger = logging.getLogger(__name__)

def is_ipynb_checkpoint(notebook_file: PathLike):
    return ".ipynb_checkpoint" in str(notebook_file)

def notebook_to_html(notebook_path: PathLike, documentation_path: PathLike):
    os.system(f"jupyter nbconvert --output-dir='{documentation_path}' --to html {notebook_path}")

def notebook_to_html_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-file",
        type=pathlib.Path,
        help="Notebook to convert to html."
    )
    parser.add_argument(
        "-doc",
        type=pathlib.Path,
        help="Directory where the html file will be saved. Defaults to the current directory.",
        default=".",
    )
    args = parser.parse_args()

    if args.file is None or args.file.suffix != ".ipynb":
        _logger.warn("You must specify a valid notebook (.ipynb file) to convert.")
        exit()

    notebook_to_html(args.file, args.doc)

def notebooks_to_html_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dir",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument(
        "-doc",
        type=pathlib.Path,
        help="Directory where the html files will be saved. Defaults to the current directory.",
        default=".",
    )
    args = parser.parse_args()

    for notebook_file in args.dir.rglob("*.ipynb"):
        # Ignores ipynb checkpoints
        if not is_ipynb_checkpoint(notebook_file):
            notebook_to_html(notebook_file, args.doc)

def strip_notebook(notebook_path: PathLike):
    os.system(f"jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace {notebook_path}")

def strip_notebook_cli():
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-file",
        type=pathlib.Path,
        help="Notebook to strip."
    )
    args = parser.parse_args()

    if args.file is None or args.file.suffix != ".ipynb":
        _logger.warn("You must specify a valid notebook (.ipynb file) to strip.")
        exit()

    strip_notebook(args.file)

def strip_notebooks_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-dir",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    args = parser.parse_args()

    for notebook_file in args.dir.rglob("*.ipynb"):
        # Ignores ipynb checkpoints
        if not is_ipynb_checkpoint(notebook_file):
            strip_notebook(notebook_file)

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
