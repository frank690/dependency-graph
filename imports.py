from pathlib import Path
from typing import List, Dict

import re
from constants import (
    ROOT,
    TARGET,
    GET_IMPORT_NAME_PATTERN,
    GET_ALL_IMPORTS_PATTERN,
    GET_LEVELS_PATTERN,
)


def get_files(root: str = ROOT, file_type: str = 'py') -> List[str]:
    """
    get all files (also in sub-directories) from given root path with a specific file_type.
    Return them as a list of strings.
    :param root: path to look for files
    :param file_type: type of files to collect
    :return: list of strings containing the path of each file
    """
    return [file for file in Path(root).glob(f'**/*.{file_type}')]


def from_directory_to_import_name(file: Path) -> str:
    """
    transform given directory file path to an import-like format.
    __init__.py files point to their parent directory.
    e.g. /my/super/fancy/__init__.py -> my.super.fancy
    :param file: path of file to transform
    :return: import name of file
    """
    file = str(file.relative_to(ROOT))

    if file.endswith('__init__.py'):
        file = file[:-11]

    name = TARGET + ''.join(['.' + f for f in file.split('/') if len(f) > 0])

    if name.endswith('.py'):
        return name[:-3]
    return name


def get_all_imports(file: Path) -> List[str]:
    """
    read the content of a file and extract all import patterns.
    :param file: path to file
    :return: list of strings. each string is an import statement within the given file.
    """
    matches = []
    with file.open('r') as f:
        lines = f.read()
    for match in re.finditer(pattern=GET_ALL_IMPORTS_PATTERN, string=lines):
        matches.append(match.group())
    return matches


def remove_external_imports(imports: List[str]) -> List[str]:
    """
    removes imports from external libraries.
    this is achieved by checking if the given import name contains the TARGET directory
    (main directory of repo to analyze).
    :param imports: list of imports as strings.
    :return: list of imports (as strings) without external libraries.
    """
    return [match for match in imports if TARGET in match]


def from_imports_to_import_names(imports: List[str]) -> List[str]:
    """
    extract import names from given imports.
    e.g. from my.fancy.module import someclass -> my.fancy.module
    :param imports:
    :return:
    """
    compiler = re.compile(pattern=GET_IMPORT_NAME_PATTERN)
    return [match.group(1) for match in (compiler.match(imp) for imp in imports) if match]


def get_imports(file: Path) -> List[str]:
    """
    get all imports from a file, remove external libraries and get the import name.
    :param file: path to file to extract import names from.
    :return: list of import names from a specific file.
    """
    all_imports = get_all_imports(file=file)
    internal_imports = remove_external_imports(imports=all_imports)
    return from_imports_to_import_names(imports=internal_imports)


def get_levels(file: str) -> Dict:
    """

    :param file:
    :return:
    """
    compiler = re.compile(pattern=GET_LEVELS_PATTERN)
    levels = compiler.findall(string=file)
