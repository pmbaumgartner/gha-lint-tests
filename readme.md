TODO:
- project.yml
  - dirs: assets, corpus, scripts, components, configs, package, models
  - minimal versions of files in each of those with example commands
  - a setup command that git inits (if not already there), checks git lfs, does the editable install.
  - 
- .gitignore
  - models
  - package
  - corpus
- .gitattributes (lfs)
- setup.py (and setup command)
- gh actions
  - flake8
  - flake8-print
  - flake8-fixme
  - flake8-docstrings
  - black
  - isort
  - mypy
  - pyright?
- requirements.txt
  - wheel?
  - setuptools
  - 
- requirements-dev.txt
- https://github.com/explosion/terraform-workspace-containers/commit/51ee0f1c760b77fea49c3423bdd62def8b3cce8f - (allow push from repo)





# pre-commit

Install from dev
`pre-commit install --hook-type manual`

`pre-commit run --all-files`

Have to initially commit the files.


# two files: run and check
# run will run them 
pre-commit run --all-files --hook-stage manual -c .pre-commit-config.run.yaml

This can be good for local use if you want isort and black to do their things.

# check will check them

`pre-commit run --all-files --color never --hook-stage manual -c .pre-commit-config.run.yaml`