# stitch


## Setup instructions

- clone the repo
- install [uv](https://docs.astral.sh/uv/)
- cd into the repo and run `uv sync`
- activate the virtual env with `source .venv/bin/activate`
- install the pre-commit hooks with `pre-commit install`
- whenever you want to add a new package to the project, instead of `pip install <package>` use `uv add <package` as this automatically updates the pyproject.toml file and the uv.lock file
- good to go!
