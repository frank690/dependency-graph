"""
Main module to run the dependency-graph
"""

__all__ = [
    "start",
    "pre_commit_start",
]

import os
import sys
from typing import List, Optional

from tqdm import tqdm

from dependency_graph.cli import parse
from dependency_graph.graph import generate
from dependency_graph.imports import (
    from_directory_to_import_name,
    get_files,
    get_imports,
    get_levels,
)


def run(
    repository: str,
    level: int,
    output: str,
    git_add: bool = False,
    exclude: Optional[List[str]] = None,
):
    """
    Run the dependency-graph to analyze a given repository.
    :param repository: repository to analyze.
    :param level: module name level for coloring all nodes.
    :param output: output file to create (with extension).
    :param git_add: flag to indicate if resulting graph file should be automatically added to current commit
    (if file is already tracked).
    :param exclude: optional list of strings of (sub)folders to exclude from analysis.
    """
    try:
        imports = {}
        files = get_files(root=repository, exclude=exclude)

        for file in tqdm(files):
            name = from_directory_to_import_name(file=file, root=repository)
            imports[name] = {
                "levels": get_levels(name=name),
                "targets": get_imports(file=file, root=repository, exclude=exclude),
            }

        generate(data=imports, level=level, target=output)
        print(f"Graph of {repository} was generated to {output}. Good bye.")

        if git_add:
            git_add_graph(output=output)

        sys.exit(0)
    except Exception:
        print("Unexpected error:", sys.exc_info())
        sys.exit(1)


def git_add_graph(output: str):
    """
    In case pre-commit is used to run, the resulting graph might be part of the current repository.
    In this case we need to add the updated graph to the current commit, otherwise the commit fails.
    If the graph file (output of generate()) seems to be un-tracked, then there is no need to do anything.
    Note: usage of git is assumed.
    :param output: generated graph file.
    """
    try:
        tracked_files = os.popen("git ls-files").read().splitlines()
        print(tracked_files)
        if output in tracked_files:
            os.popen(f"git add {output}")
    except Exception:
        print("Unexpected error:", sys.exc_info()[0])
        sys.exit(1)


def start():
    """
    Starting point for regular usage.
    """
    args = parse()

    if args.repository is None:
        print(
            "Please provide a directory path to the repository you would like to analyze."
        )
        sys.exit(1)

    run(
        repository=args.repository,
        level=args.level,
        output=args.output,
        exclude=args.exclude,
        git_add=False,
    )


def pre_commit_start():
    """
    Starting point for pre-commit hooks.
    """
    args = parse()

    if args.repository is None:
        print(
            "Please provide a directory path to the repository you would like to analyze."
        )
        sys.exit(1)

    run(
        repository=args.repository,
        level=args.level,
        output=args.output,
        exclude=args.exclude,
        git_add=True,
    )


if __name__ == "__main__":
    start()
