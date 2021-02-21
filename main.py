from pathlib import Path
from typing import List

import re

ROOT = '/Users/frankeschner/Documents/Projects/df-lib-python/datafactory/'
TARGET = Path(ROOT).stem
GET_ALL_IMPORTS_PATTERN = '(from\s+[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)*\s+){0,1}import\s+(([A-Za-z0-9_]+)|(\((\s+[A-Za-z0-9_]+\,\s+)+\)))'
GET_IMPORT_NAME_PATTERN = 'from\s+([A-Za-z0-9_.]+)\s+import'


def get_files(root: str = ROOT, file_type: str = 'py') -> List[str]:
    """

    :param root:
    :param file_type:
    :return:
    """
    return [file for file in Path(root).glob(f'**/*.{file_type}')]


def from_directory_to_import_name(file: Path) -> str:
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
    for match in re.finditer(pattern=GET_ALL_IMPORTS_PATTERN, string=lines):
        matches.append(match.group())
    return matches


def remove_external_imports(imports: List[str]) -> List[str]:
    """

    :param imports:
    :return:
    """
    return [match for match in imports if TARGET in match]


def from_imports_to_import_names(imports: List[str]) -> List[str]:
    """

    :param imports:
    :return:
    """
    compiler = re.compile(pattern=GET_IMPORT_NAME_PATTERN)
    return [match.group(1) for match in (compiler.match(imp) for imp in imports) if match]


def get_imports(file: Path) -> List[str]:
    """

    :param file:
    :return:
    """
    all_imports = get_all_imports(file=file)
    internal_imports = remove_external_imports(imports=all_imports)
    return from_imports_to_import_names(imports=internal_imports)


if __name__ == '__main__':
    imports = {}
    files = get_files()

    for file in files:
        name = from_directory_to_import_name(file=file)
        imports[name] = get_imports(file=file)

    with open('output.csv', 'w') as e:
        e.write("target;source\n")
        for module, imps in imports.items():
            for imp in imps:
                e.write(f"{module};{imp}\n")
