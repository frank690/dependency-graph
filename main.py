from pathlib import Path
from typing import List
import re

ROOT = '/Users/frankeschner/Documents/Projects/df-lib-python/datafactory/'
PATTERN = '(from\s+[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)*\s+){0,1}import\s+(([A-Za-z0-9_]+)|(\((\s+[A-Za-z0-9_]+\,\s+)+\)))'
COMPILER = re.compile(pattern=PATTERN, flags=re.IGNORECASE)


def get_files(root: str = ROOT, file_type: str = 'py') -> List[str]:
    """

    :param root:
    :param file_type:
    :return:
    """
    return [file for file in Path(root).glob(f'**/*.{file_type}')]


def get_imports(file: Path) -> List[str]:
    """

    :param file:
    :return:
    """
    matches = []
    with file.open('r') as f:
        lines = f.read()
    for match in re.finditer(pattern=PATTERN, string=lines):
        matches.append(match.group())
    return matches, lines


if __name__ == '__main__':
    files = get_files()
    for file in files:
        m = get_imports(file=file)
        a = 1
