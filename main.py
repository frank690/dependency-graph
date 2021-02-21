from pathlib import Path
from typing import List
import re

ROOT = '/Users/frankeschner/Documents/Projects/df-lib-python/datafactory/'
TARGET = Path(ROOT).stem
PATTERN = '(from\s+[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)*\s+){0,1}import\s+(([A-Za-z0-9_]+)|(\((\s+[A-Za-z0-9_]+\,\s+)+\)))'
COMPILER = re.compile(pattern=PATTERN, flags=re.IGNORECASE)


def get_files(root: str = ROOT, file_type: str = 'py') -> List[str]:
    """

    :param root:
    :param file_type:
    :return:
    """
    return [file for file in Path(root).glob(f'**/*.{file_type}')]


def get_import_name(file: Path) -> str:
    """

    :param file:
    :return:
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

    :param file:
    :return:
    """
    matches = []
    with file.open('r') as f:
        lines = f.read()
    for match in re.finditer(pattern=PATTERN, string=lines):
        matches.append(match.group())
    return matches


def remove_external_imports(imports: List[str]) -> List[str]:
    """

    :param imports:
    :return:
    """
    return imports


def get_imports(file: Path) -> List[str]:
    """

    :param file:
    :return:
    """
    all_imports = get_all_imports(file=file)
    return remove_external_imports(imports=all_imports)


if __name__ == '__main__':
    imports = {}
    files = get_files()

    for file in files:
        name = get_import_name(file=file)
        imports[name] = get_imports(file=file)
