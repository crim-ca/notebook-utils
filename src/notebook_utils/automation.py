import argparse
import logging
import nbformat
import pathlib
import subprocess
import sys
import typing

PathLike = typing.TypeVar("PathLike", str, pathlib.Path)

_logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s - %(message)s", level=logging.ERROR)

def is_ipynb_checkpoint(notebook_file: PathLike):
    return ".ipynb_checkpoint" in str(notebook_file)

def run_notebook(notebook_path: PathLike):
    return subprocess.run(["jupyter", "nbconvert", "--to", "notebook", "--inplace", "--execute", "--ExecutePreprocessor.timeout=600", f"{notebook_path}"], capture_output=True, text=True)

def run_notebook_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        help="Notebook to run."
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    if args.file is None or args.file.suffix != ".ipynb":
        _logger.error("You must specify a valid notebook (.ipynb file) to run.")
        sys.exit(1)

    _logger.info("Running %s.", args.file)

    completed_process = run_notebook(args.file)
    if completed_process.returncode != 0:
        _logger.error("An error occured while running the file %s.", args.file)
        _logger.warning(completed_process.stderr)
        _logger.warning(completed_process.stdout)
        sys.exit(1)

    sys.exit(0)

def run_notebooks_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--directory",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    exit_status = []
    for notebook_file in args.directory.rglob("*.ipynb"):
        # Ignores ipynb checkpoints
        if not is_ipynb_checkpoint(notebook_file):
            _logger.info("Running %s...", notebook_file)
            completed_process = run_notebook(notebook_file)
            if completed_process.returncode == 0:
                exit_status.append(0)
            else:
                exit_status.append(1)
                _logger.error("An error occured while running %s.", notebook_file)
    sys.exit(any(exit_status))

def notebook_to_html(notebook_path: PathLike, output_path: PathLike):
    return subprocess.run(["jupyter", "nbconvert", f"--output-dir='{output_path}'", "--to", "html", f"{notebook_path}"], capture_output=True, text=True)

def notebook_to_html_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        help="Notebook to convert to html."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        help="Directory where the html file will be saved. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    if args.file is None or args.file.suffix != ".ipynb":
        _logger.error("You must specify a valid notebook (.ipynb file) to convert.")
        sys.exit(1)

    _logger.info("Converting %s.", args.file)

    completed_process = notebook_to_html(args.file, args.output)
    if completed_process.returncode != 0:
        _logger.error("An error occured while stripping the file %s.", args.file)
        _logger.warning(completed_process.stderr)
        _logger.warning(completed_process.stdout)
        sys.exit(1)

    sys.exit(0)

def notebooks_to_html_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--directory",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=pathlib.Path,
        help="Directory where the html files will be saved. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    exit_status = []
    for notebook_file in args.directory.rglob("*.ipynb"):
        # Ignores ipynb checkpoints
        if not is_ipynb_checkpoint(notebook_file):
            _logger.info("Converting %s...", notebook_file)
            completed_process = notebook_to_html(notebook_file, args.output)
            if completed_process.returncode == 0:
                exit_status.append(0)
            else:
                exit_status.append(1)
                _logger.error("An error occured while converting %s.", notebook_file)
                
    sys.exit(any(exit_status))

def strip_notebook(notebook_path: PathLike):
    return subprocess.run(["jupyter", "nbconvert", "--ClearOutputPreprocessor.enabled=True", "--inplace", f"{notebook_path}"], capture_output=True, text=True)

def strip_notebook_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=pathlib.Path,
        help="Notebook to strip."
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    if args.file is None or args.file.suffix != ".ipynb":
        _logger.error("You must specify a valid notebook (.ipynb file) to strip.")
        sys.exit(1)

    _logger.info("Stripping %s.", args.file)

    completed_process = strip_notebook(args.file)
    if completed_process.returncode != 0:
        _logger.error("An error occured while stripping the file %s.", args.file)
        sys.exit(1)

    sys.exit(0)

def strip_notebooks_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--directory",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    exit_status = []
    for notebook_file in args.directory.rglob("*.ipynb"):
        # Ignores ipynb checkpoints
        if not is_ipynb_checkpoint(notebook_file):
            _logger.info("Stripping %s...", notebook_file)

            completed_process = strip_notebook(notebook_file)
            if completed_process.returncode == 0:
                exit_status.append(0)
            else:
                exit_status.append(1)
                _logger.error("An error occured while stripping %s.", notebook_file)

    sys.exit(any(exit_status))

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
        "-d",
        "--directory",
        type=pathlib.Path,
        help="Directory where to recursively look for notebooks. Defaults to the current directory.",
        default=".",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Output logging details.")
    args = parser.parse_args()

    if args.verbose:
        _logger.setLevel(logging.INFO)

    are_stripped = []
    for notebook_file in args.directory.rglob("*.ipynb"):
        if not is_ipynb_checkpoint(notebook_file):
            _logger.info("Checking %s...", notebook_file)
            if notebook_is_stripped(notebook_file):
                are_stripped.append(True)
            else:
                are_stripped.append(False)
                _logger.error("Notebook file %s is not stripped.", notebook_file)

    sys.exit(not all(are_stripped))
