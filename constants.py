COMMENTS_PATTERN = r'\#.*\s'
GET_ALL_IMPORTS_PATTERN = r'(from\s+[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)*\s+){0,1}import\s+(([A-Za-z0-9_*]+)|(\((\s+[A-Za-z0-9_*]+(\,)?\s+)+\)))'
GET_IMPORT_NAME_PATTERN = r'from\s+([A-Za-z0-9_.]+)\s+import'
GET_LEVELS_PATTERN = r'[A-Za-z0-9_]+'
DISTINCT_COLOR_MAP = [
    '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0',
    '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8',
    '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff',
    ]
