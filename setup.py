from setuptools import find_packages, setup

SRC_DIR = "src"

setup(
    name="notebook_utils",
    description="Functions and utilities for machine learning and data science.",
    author="Computer Research Institute of Montreal (CRIM)",
    license='MIT',
    version="0.1.0",
    packages=find_packages(where=SRC_DIR, exclude=["tests"]),
    package_dir={"": SRC_DIR},
    entry_points={
        "console_scripts": [
            "crim_notebooks_are_stripped = notebook_utils.automation:notebooks_are_stripped_cli"
        ]
    },
)
