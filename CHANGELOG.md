Changelog
=========

Version 0.2.1
-------------
- Exclude argument now also filters edges. previously it was possible that filters removed some nodes but not the edges pointing to them (from other nodes) resulting in ValueErrors on the python-igraph interface.

Version 0.2.0
-------------
- Using this class as a pre-commit hook is now using another entrance point (see setup.py). This causes to automatically add the resulting file if it was already tracked.

Version 0.1.11
-------------
- Modified hook to start automatically after (!) commit.

Version 0.1.10
-------------
- Modified hook to be started manually via ```pre-commit run --hook-stage manual dependency-graph```

Version 0.1.9
-------------
- Introduced --exclude (-e) argument in parser. This allows filtering of folders that shall not be analyzed.
- Updated TODO list.

Version 0.1.8
-------------
- Modified after mirroring into sms digital.

Version 0.1.7
-------------
- Modified argumentparser in cli.py to ignore additional provided input. That is a much better way of doing it.

Version 0.1.6
-------------
- Added args to argumentparser in cli.py to handle additionally provided input that is not needed.
- Modified pre-commit hook yaml.

Version 0.1.5
-------------
- Added start() to main.py to have an uniform entry point for everyone.
- Modified setup.py as well as pre-commit-hooks to make it work properly.
- Introduced isort and applied it to all the files as well.

Version 0.1.4
-------------
- Added .pre-commit-hooks.yaml to use this repo as hook.
- Renamed .pre-commit-config.yml to .yaml.

Version 0.1.3
-------------
- main.py now has proper exits and messages.
- Added repo tag
- fixed black version in pre-commit

Version 0.1.2
-------------
- Enhanced cli help descriptions
- Added more things to TODO list
- main init file is now offering run method

Version 0.1.1
-------------
- Moved all py files into subfolder
- Introduced black and isort

Version 0.1.0
-------------
- Added CHANGELOG.md
- Implemented first working version
- Implemented CLI
- Added setup.py

Version 0.0.1
-------------
- Initial commit
 