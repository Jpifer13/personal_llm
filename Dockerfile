# syntax=docker/dockerfile:1.2
FROM public.ecr.aws/lambda/python:3.12
# FROM public.ecr.aws/lambda/provided:al2023
# FROM public.ecr.aws/lambda/nodejs:20

SHELL ["/bin/bash", "-c"]

# RUN apt-get install curl \
#     && apt-get install autoremove

RUN dnf install -y nodejs

RUN pip3.12 install awslambdaric

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/etc/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.7.1

ENV POETRY_PATH="${POETRY_HOME}/bin/poetry"

WORKDIR ${LAMBDA_TASK_ROOT}

# following https://python-poetry.org/docs/master/#installation
RUN curl -sSL https://install.python-poetry.org | python3.12 -
RUN cd /usr/local/bin && ln -s ${POETRY_PATH} && chmod +x ${POETRY_PATH}

COPY ./ui/package.json ./ui/package-lock.json ./ui/
RUN cd ./ui && npm install

# copy the lock and toml files, install
#
# Do we have to install in ${LAMBDA_TASK_ROOT}?
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry config virtualenvs.create false \
	&& poetry install -vvv --no-interaction --no-ansi --no-root

# copy code (we should be more selective here, even with .dockerignore)
COPY . ${LAMBDA_TASK_ROOT}

# build the frontend to /static and remove the source
RUN cd ./ui && npm run build && rm -rf ./ui

# ENV PYTHONPATH=${PYTHONPATH}:/${LAMBDA_TASK_ROOT}/application

ENTRYPOINT [ "/usr/bin/python3.12", "-m", "awslambdaric" ]
CMD [ "app.handler" ]
