"""
This module contains functionality for the cli of this repository.
"""

from argparse import ArgumentParser


def parse():
    parser = ArgumentParser(
        description="dependency-graph that can be used to visualize the dependencies "
        "within a given repository by drawing a network graph."
    )

    parser.add_argument(
        "-r",
        "--repository",
        type=str,
        help="Path to repository that should be analyzed.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="output.svg",
        help="Path with extension of output file.",
    )
    parser.add_argument(
        "-l",
        "--level",
        type=int,
        default=0,
        help="Module name level that defines group (of nodes) coloring.",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        type=str,
        nargs="*",
        help="Define list of (sub)folders that should be ignored during the analysis.",
    )

    args, _ = parser.parse_known_args()

    return args
