"""
This module contains functionality for the cli of this repository.
"""

from argparse import ArgumentParser


def parse():
    parser = ArgumentParser(description='dependency-graph')

    parser.add_argument(
        '-r', '--repository', type=str,
        help='Path to repository that should be analyzed.'
    )
    parser.add_argument(
        '-o', '--output', type=str, default='output.svg',
        help='Path with extension of output file.'
    )
    parser.add_argument(
        '-l', '--level', type=int, default=0,
        help='Module name level that defines group (of nodes) coloring.'
    )

    return parser.parse_args()
