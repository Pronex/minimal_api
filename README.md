# minimal_api

Minimal template for FastAPI container app on azure.

Built on top of [FastAPI](https://fastapi.tiangolo.com/) on **python 3.10**.

[
    ![Open in Remote - Containers](
        https://img.shields.io/static/v1?label=Remote%20-%20Containers&message=Open&color=blue&logo=visualstudiocode
    )
](
    https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/Pronex/minimal_api
)

Included:

- 💻 boilerplate for FastAPI app
- 🐳 dockerfile for containerization
- 🏗️ terraform files for infrastructure -> azure container app
- 🐈‍⬛ github actions workflow for CI/CD -> QA, TF, CI
- 📦 VScode devcontainer for development
- 🪲 VScode debugging configuration for FastAPI
- 🧪 testing with `tox` and `pytest`
- 🧹 linting and formatting with `yapf` and `mypy`
- ☁️ space for your own code

**Get started:**

1. Clone the repo
2. Replace all `*.example` files with the correct names and values for your case
3. Replace all `minimal_api` with the name of your app and add your own code
4. Build and run the container locally
5. Deploy the infrastructure to Azure
6. Check if the app is running on Azure

## API Documentation

Documentation for the API is [automagically](https://fastapi.tiangolo.com/tutorial/first-steps/#interactive-api-docs) served whenever the API is running and can be found at: [http://{api}:{port}/docs](http://{api}:{port}/docs) or [http://{api}:{port}/redoc](http://{api}:{port}/redoc).

## Authentication

Authentication to the API is HTTP BasicAuth defined by environment variables in a `config.yml` file:

    ```yaml
    uname: "username"
    pword: "password"
    ```

## Infrastructure

**Requirements:** `tf.env` file with the following variables defined:

    export ARM_CLIENT_ID=appId
    export ARM_CLIENT_SECRET=password
    export ARM_SUBSCRIPTION_ID=subscription_id
    export ARM_TENANT_ID=tenantId

Login with `python _az_login.py` and then `source tf.env`. This will set the environment variables for the current shell, which terraform will need to init.

Alternatively, login to Azure with `az login` and select the correct subscription with `az account set --subscription <subscription_id>`. You should use a service principal for this. You can create one with `az ad sp create-for-rbac --name <name> --role contributor --scopes /subscriptions/<subscription_id>`. You can then login with `az login --service-principal --username <appId> --password <password> --tenant <tenantId>`.

This repository is built and deployed using [Terraform](https://www.terraform.io/). The files are located in the `.tf` folder. Either `cd` into the folder or use the `-chdir=.tf` flag to run the commands from the root of the repo.

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

You can destroy the infrastructure using the following command `terraform destroy`.

You might need to have a set of variables defined in a `terraform.tfvars` or `<name>.auto.tfvars` file. You can also pass variables on the command line with `-var="name=value"`.

## Build

**Requirements:** `config.py` (or environment variables) file with *at least* the following variables defined:

        ```python
        uname = "username"
        pword = "password"
        ```

Ideally this can be developed in a devcontainer using VScode. You can use the `devcontainer.json` file included in the repo to get started. You'll need to install the [Remote - Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension for VScode. You can then open the project in a container by clicking the green button in the bottom left corner of VScode and selecting "Remote-Containers: Open Folder in Container...". You'll then be prompted to select the folder to open in a container. Select the folder containing this repo and you're good to go.

Otherwise, you should use a virtualenv to install any dependencies locally (for development). You'll find the docs [here](https://docs.python.org/3/library/venv.html) and a quick intro [here](https://realpython.com/python-virtual-environments-a-primer/#what-is-a-virtual-environment). Create a virtual environment with `python -m venv .venv` (Win) and source it with `.\.venv\Scripts\Activate.ps1` (PS) or `python3 -m venv .venv` (linux) and aource it with `source .venv/bin/activate`. You can then install all requirements with `pip install -r requirements.txt`.

To run the app in "debug mode" locally such that the server reloads the at file change, use:

    ```bash
    uvicorn api:app --port 8080 --reload
    ```

You can also create a FastAPI debugging configuration for VScode with `"module": "uvicorn", "args": ["api:app", "--port=8080", "--reload"]` or using the `launch.json` file included in the repo.

To build and run the container locally do:

    ```bash
    docker build -t minimal_api:latest .
    docker run -it --name minimal_api -p 8080:8080 minimal_api:latest
    # docker rm minimal_api # to remove the container if --rm didn't work
    ```

-> one liner for debugging purposes:

    ```bash
    docker rm minimal_api; docker build -t minimal_api:latest .; docker run -it --name minimal_api -p 8080:8080 minimal_api:latest
    ```

This can also be done using the `docker_run.py` script included in the repo. You can run the script with `python docker_run.py` or `python docker_run.py --help` to get more info.

You'll then find the application running at [http://localhost:8080/](http://localhost:8080/) or similar.

## Testing & QA

Testing is done with `tox` and `pytest`. You can run the tests with `tox` or `pytest` (or `pytest -v` for more verbosity). You can also run the tests with `pytest --cov=src --cov-report=html` to get a coverage report in html format

Get missing stubs with `mypy --install-types`.

Otherwise the GitHub actions workflow will run the tests and linting on every push to the main branch.

## Build and push to production

To build and push the container to production do a git merge to the branch `main`. And then do your thing.

The command to run in production is:

    ```bash
    uvicorn api:app --host 0.0.0.0 --port 8080
    ```

OR as a container:

    ```bash
    docker run -d --name minimal_api -p 8080:8080 --restart=always minimal_api:latest
    ```

... assuming the environment variables are already present.

## Code formatting

The google code style is used for formatting. You can use the following command to format the code:

    ```bash
    tox -e format
    ```

## Maintainers

- @pronex
