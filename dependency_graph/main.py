"""
Main module to run the dependency-graph
"""

__all__ = [
    "run",
]

import sys

from tqdm import tqdm

from dependency_graph.cli import parse
from dependency_graph.graph import generate
from dependency_graph.imports import (
    from_directory_to_import_name,
    get_files,
    get_imports,
    get_levels,
)


def run(repository: str, level: int, output: str):
    """
    Run the dependency-graph to analyze a given repository.
    :param repository: repository to analyze.
    :param level: module name level for coloring all nodes.
    :param output: output file to create (with extension).
    """
    try:
        imports = {}
        files = get_files(root=repository)

        for file in tqdm(files):
            name = from_directory_to_import_name(file=file, root=repository)
            imports[name] = {
                "levels": get_levels(name=name),
                "targets": get_imports(file=file, root=repository),
            }

        generate(data=imports, level=level, target=output)
        print(f"Graph of {repository} was generated to {output}. Good bye.")
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
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
    )
