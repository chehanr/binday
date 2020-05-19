FROM python:3.8.2-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION 1.0.5

# set work directory
WORKDIR /usr/src/app

# install dependencies
RUN apk add --no-cache gcc libffi-dev musl-dev openssl-dev
RUN pip install --upgrade pip
RUN pip install "poetry==$POETRY_VERSION"

# copy files for poetry
COPY pyproject.toml poetry.lock ./

# install python dependencies
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# copy entrypoint.sh
COPY ./scripts/entrypoint.sh ./

# copy project
COPY . ./

# run entrypoint.sh
ENTRYPOINT ["./scripts/entrypoint.sh"]