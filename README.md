# minimal_api

Minimal template for FastAPI container app on azure.

Built on top of [FastAPI](https://fastapi.tiangolo.com/) on **python 3.10**.

## API Documentation

Documentation for the API is [automagically](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs) served whenever the API is running and can be found at: [http://{api}:{port}/docs](http://{api}:{port}/docs) or [http://{api}:{port}/redoc](http://{api}:{port}/redoc).

## Authentication

Authentication to the API is HTTP BasicAuth defined by environment variables in a `config.yml` file:

    ```yaml
    username: "username"
    password: "password"
    ```

## Infrastructure

This repository is built and deployed using [Terraform](https://www.terraform.io/).

You can deploy the infrastructure using the following commands:

    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

You shouldn't forget to format and validate your code before committing:

    ```bash
    terraform fmt
    terraform validate
    ```

You need to have a set of variables defined in a `terraform.tfvars` file. You can use the `terraform.tfvars.example` file as a template.

## Build

You should use a virtualenv to install any dependencies locally (for development). You'll find the docs [here](https://docs.python.org/3/library/venv.html) and a quick intro [here](https://realpython.com/python-virtual-environments-a-primer/#what-is-a-virtual-environment). Create a virtual environment with `python -m venv .venv` (Win) and source it with `.\.venv\Scripts\Activate.ps1` (PS) or `python3 -m venv .venv` (linux) and aource it with `source .venv/bin/activate`. You can then install all requirements with `pip install -r requirements.txt`.

To run the app in "debug mode" locally such that the server reloads the at file change, use:

    ```bash
    uvicorn api:app --port 8080 --reload
    ```

You can also create a FastAPI debugging configuration for VScode with `"module": "uvicorn", "args": ["api:app", "--port=8080", "--reload"]` or using the `launch.json` file included in the repo.

To build and run the container locally do:

    ```bash
    podman build -t minimal_api:latest .
    podman run -it --name minimal_api -p 8080:8080 minimal_api:latest
    # podman rm minimal_api # to remove the container if --rm didn't work
    ```

-> one liner for debugging purposes:

    ```bash
    podman rm minimal_api; podman build -t minimal_api:latest .; podman run -it --name minimal_api -p 8080:8080 minimal_api:latest
    ```

You'll then find the application running at [http://localhost:8080/](http://localhost:8080/).

## Testing & QA

Testing is done with `tox` and `pytest`. You can run the tests with `tox` or `pytest` (or `pytest -v` for more verbosity). You can also run the tests with `pytest --cov=src --cov-report=html` to get a coverage report in html format

Get missing stubs with `mypy --install-types`.

## Build and push to production

To build and push the container to production do a git merge to the branch `main`. And then do your thing.

The command to run in production is:

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8080
    ```

OR as a container:

    ```bash
    podman run -d --name minimal_api -p 8080:8080 --restart=always minimal_api:latest
    ```

... assuming the environment variables are already present.

## Code formatting

The google code style is used for formatting. You can use the following command to format the code:

    ```bash
    tox -e format
    ```

## Maintainers

- @pronex
