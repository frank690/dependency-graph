from imports import (
    get_files,
    from_directory_to_import_name,
    get_imports,
    get_levels,
)

from graph import generate


if __name__ == '__main__':
    imports = {}
    files = get_files()

    for file in files:
        name = from_directory_to_import_name(file=file)
        imports[name] = get_imports(file=file)

    generate(data=imports)
