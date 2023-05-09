# minimal_api - boilerplate for a minimal API
# Author: pronex

# set base image
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# copy the requirements file to the working directory
RUN mkdir -p /src/app
COPY ./requirements.txt /src/requirements.txt

# set the working directory in the container
WORKDIR /src

# install dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the other dependencies file to the working directory
COPY api.py config.py config.yml /src
COPY ./app /src/app

# entrypoint and starting command
# --proxy-headers will tell Uvicorn to trust the headers sent by TLS offloading proxy
CMD ["uvicorn", "api:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]