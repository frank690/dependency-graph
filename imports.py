"""
Module to import and clean the content of all the python files inside the target repository.
"""

from pathlib import Path
from typing import List, Dict, Set

import re
from constants import (
    COMMENTS_PATTERN,
    DOCSTRING_PATTERN,
    GET_IMPORT_NAME_PATTERN,
    GET_ALL_IMPORTS_PATTERN,
    GET_LEVELS_PATTERN,
)


def get_files(root: str, file_type: str = 'py') -> Set[str]:
    """
    get all files (also in sub-directories) from given root path with a specific file_type.
    Return them as a list of strings.
    :param root: path to look for files
    :param file_type: type of files to collect
    :return: list of strings containing the path of each file
    """
    return set([file for file in Path(root).glob(f'**/*.{file_type}') if '/venv/' not in file.name])


def from_directory_to_import_name(file: Path, root: str) -> str:
    """
    transform given directory file path to an import-like format.
    __init__.py files point to their parent directory.
    e.g. /my/super/fancy/__init__.py -> my.super.fancy
    :param file: path of file to transform
    :param root: main directory to look for imports
    :return: import name of file
    """
    file = str(file.relative_to(root))

    if file.endswith('__init__.py'):
        file = file[:-11]

    name = Path(root).stem + ''.join(['.' + f for f in file.split('/') if len(f) > 0])

    if name.endswith('.py'):
        return name[:-3]
    return name


def read_file(file: Path) -> str:
    """
    read a given file and return its content
    :param file: file to read as pathlib Path
    :return: content of file as string
    """
    with file.open('r') as f:
        lines = f.read()
    return lines


def remove_comments(lines: str) -> str:
    """
    removes all comments from a given string until the next line break.
    :param lines: string to remove comments from
    :return: string without comments
    """
    return re.subn(pattern=COMMENTS_PATTERN, repl=r'\n', string=lines)[0]


def remove_docstrings(lines: str) -> str:
    """
    removes all docstrings from a given string until the next line break.
    :param lines: string to remove docstrings from
    :return: string without docstrings
    """
    return re.subn(pattern=DOCSTRING_PATTERN, repl=r'\n', string=lines)[0]


def get_all_imports(file: Path) -> List[str]:
    """
    read the content of a file and extract all import patterns.
    :param file: path to file
    :return: list of strings. each string is an import statement within the given file.
    """
    matches = []
    lines = read_file(file=file)
    lines = remove_comments(lines=lines)
    lines = remove_docstrings(lines=lines)
    for match in re.finditer(pattern=GET_ALL_IMPORTS_PATTERN, string=lines):
        matches.append(match.group())
    return matches


def remove_external_imports(imports: List[str], root: str) -> List[str]:
    """
    removes imports from external libraries.
    this is achieved by checking if the given import name contains the stem of the root directory
    (main directory of repo to analyze).
    :param imports: list of imports as strings.
    :param root: main directory to look for imports
    :return: list of imports (as strings) without external libraries.
    """
    return [match for match in imports if Path(root).stem in match]


def from_imports_to_import_names(imports: List[str]) -> List[str]:
    """
    extract import names from given imports.
    e.g. from my.fancy.module import someclass -> my.fancy.module
    :param imports:
    :return:
    """
    compiler = re.compile(pattern=GET_IMPORT_NAME_PATTERN)
    return [match.group(1) for match in (compiler.match(imp) for imp in imports) if match]


def get_imports(file: Path, root: str) -> List[str]:
    """
    get all imports from a file, remove external libraries and get the import name.
    :param file: path to file to extract import names from.
    :param root: main directory to look for imports
    :return: list of import names from a specific file.
    """
    all_imports = get_all_imports(file=file)
    internal_imports = remove_external_imports(imports=all_imports, root=root)
    return from_imports_to_import_names(imports=internal_imports)


def get_levels(name: str) -> Dict:
    """
    extracts the module name levels from a given module name and returns them recursively joined as a dictionary.
    e.g. some.module.with.sub -> {"0": "some", "1": "some.module", "2": "some.module.with", ... }
    :param name: module name string to extract levels from.
    :return: module levels recursively joined in a dictionary
    """
    compiler = re.compile(pattern=GET_LEVELS_PATTERN)
    levels = compiler.findall(string=name)
    return {idx: ".".join(levels[:idx+1]) for idx in range(len(levels))}
