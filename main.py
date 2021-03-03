from imports import (
    get_files,
    from_directory_to_import_name,
    get_imports,
    get_levels,
)

import sys
from tqdm import tqdm
from graph import generate

if __name__ == '__main__':
    if len(sys.argv) == 2:
        root = sys.argv[1]
    else:
        print('Please ONLY include the directory path of the repository you want to generate a dependency graph for.')
        sys.exit(1)

    imports = {}
    files = get_files(root=root)

    for file in tqdm(files):
        name = from_directory_to_import_name(file=file, root=root)
        imports[name] = {
            "levels": get_levels(name=name),
            "targets": get_imports(file=file, root=root),
        }

    generate(data=imports, level=2, target='graph.pdf')
