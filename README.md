# LAIKA Coding challenge

## Code structure of laika_pipeline

### Folders
- **db**: Contains the persistent storage layer of the project. 
- **example**: Contains code example on how to use the API.
- **lib**: Contains general helper functions.
- **pipeline**: Cintains the main object types of the pipeline.
- **test**: Contains all unittests to test the API.
- **validation**: Contains code partaining to validating logic. 

### Interface
- **api.py**: The public API to interact with the mini pipeline.
- **cli.py**: The command line interface to interacte with the mini pipeline.

## Poetry

Poetry was used as an environment packager. A simple `pyproject.toml` file is included which declares a single place how the project is built, what it depends on, and how tools should behave.

To make use of poetry:

`pip install poetry`: to install poetry

`poetry install`: will generate a poetry.lock file

Three script commands are defined in the toml file:

- `poetry run run_tests`: runs all the unittests.
- `potry run run_demo`: runs a very simple project demo.
- `poetry run_api_example`: runs some example of api usage defined.