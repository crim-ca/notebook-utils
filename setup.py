from setuptools import find_packages, setup

SRC_DIR = "src"

setup(
    name="notebook_utils",
    description="Functions and utilities for machine learning and data science.",
    author="Computer Research Institute of Montreal (CRIM)",
    license='MIT',
    version="0.2.0",
    packages=find_packages(where=SRC_DIR, exclude=["tests"]),
    package_dir={"": SRC_DIR},
    install_requires=[
        "jupyter",
        "nbformat>=5.1.3",
    ],
    entry_points={
        "console_scripts": [
            "crim_notebooks_are_stripped = notebook_utils.automation:notebooks_are_stripped_cli",
            "crim_notebook_to_html = notebook_utils.automation:notebook_to_html_cli",
            "crim_notebooks_to_html = notebook_utils.automation:notebooks_to_html_cli",
            "crim_strip_notebook = notebook_utils.automation:strip_notebook_cli",
            "crim_strip_notebooks = notebook_utils.automation:strip_notebooks_cli",
        ]
    },
)
