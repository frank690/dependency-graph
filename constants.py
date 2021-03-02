from pathlib import Path

ROOT = '/Users/frankeschner/Documents/Projects/df-lib-python/datafactory/'
TARGET = Path(ROOT).stem
GET_ALL_IMPORTS_PATTERN = r'(from\s+[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)*\s+){0,1}import\s+(([A-Za-z0-9_]+)|(\((\s+[A-Za-z0-9_]+\,\s+)+\)))'
GET_IMPORT_NAME_PATTERN = r'from\s+([A-Za-z0-9_.]+)\s+import'
GET_LEVELS_PATTERN = r'[A-Za-z0-9_]+'