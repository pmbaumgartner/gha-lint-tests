# Example sTP project

This is an end-to-end example sTP project to demonstrate the workflow and project structure we've evolved through our consulting projects. It will be continually developed and the `main` branch should always be a usable example. In addition, this repository serves as a collection of "best practices" that people can pull from piecemeal (e.g. if you only need the GitHub Actions files).

Here's what's different in this project compared to copying a project template or starting a `project.yml` from scratch:
- A `requirements-dev.txt` file with libraries that make development easier (but are not required to build the model)
- A collection of lints & checks in a manually executed [pre-commit hook](https://pre-commit.com/) to help with code consistency and documentation.
- Uses [`Git LFS`](https://git-lfs.github.com/) to store large files that don't need diffs (model weights, source data)
- An example [`typer`](https://typer.tiangolo.com/) script for commands (commonly used for data processing)
- Has relevant [`GitHub Actions`](https://docs.github.com/en/actions) for:
  - Running all the pre-commit hooks on a pull request
  - Running an end-to-end test of the main project workflow to ensure a packaged model can be installed and run
  - Publishing the model package to our internal PyPI repo (for use with the evaluation API)
  - Delivering the model code as a `.zip` file with internal data removed from the source code.
- spaCy project file (and associated configs) for a common applied project workflow: process data, train model, assemble model, evaluate, and package.
- Explanatory comments in consulting-project specific files required for the above features.

### Setup

If you want to use this as a _project template_, clone the repo into a new folder. In that folder, remove the git history with `rm -rf .git` and re-initialize git with `git init`. Create a virtual environment and activate it. Once you've activated your virtual environment:

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Once the requirements are installed, you'll need to set up pre-commit. We run the pre-commit hooks manually locally and automatically when a pull request is made. There are two files for the precommit hooks: `.pre-commit-config.check.yaml` and `.pre-commit-config.run.yaml`. The `check` hook will display any linting errors or changes that would be made by formatting tools like `black` and `isort`. It will not modify files. The `run` hook will run those same commands **and** modify any files run through the formatters. 

Install pre-commit with:

```bash
pre-commit install --allow-missing-config
```

Pre-commit only works on files that you have previously committed to the repo. Since you removed the git history when you cloned the repo, you'll need to the commit the files in the repository. Then you can run pre-commit with the following commands:

```bash
# to check and not modify files
pre-commit run --all-files --hook-stage manual -c .pre-commit-config.check.yaml

# to run and modify files
pre-commit run --all-files --color never --hook-stage manual -c .pre-commit-config.run.yaml
```

### Why run pre-commit manually locally?

If you've used pre-commit before, you'll know that the default setting is to run any hooks on an attempted commit. If you're having issues with your linters or formatters, this can get really annoying in situations where you might want to commit and push files that would not pass a check, but you want to save progress and that commit still represents a logical unit of work. 

Instead of annoyingly auto-running the hooks, the automation of running the linters occurs in CI with GitHub Actions on a pull request. It is recommended to protect the `main` branch and turn off pushes to `main`, and enforce the constraint that code changes have to come from a pull request. In this way, the pull request represents a "bundle" of code that should pass the required CI checks, so you know that any code in `main` has passed all the linters. A developer can use the pull request checks to understand which are failing, execute the `run` hook locally as outlined above to fix any formatting issues and identify linting issues needing fixes.

### Checking that example files and logic are removed

Since this is a fully functional example project, you'll want to ensure any of the example code is gone from the repository before delivery if you were actually using this for a project. You can search for the strings I used to identify this as an example with the following command:

```bash
grep -rniE --exclude=\*.{json,lock,pyc} --exclude-dir=\*/package --exclude-dir=.git "(?:stp[-_]example|example)" .
```

Alternatively, if you're using [ripgrep](https://github.com/BurntSushi/ripgrep) (which is much faster):

```bash
rg -e "(?:stp[-_]example|example)" -g '!*.json' -g '!*.lock' -g '!.git' --hidden .
```

