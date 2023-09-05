# FROM python:3.8.13-slim-
FROM python:3.10.13-slim


ARG FastAPIENV

ENV FastAPIENV=${FastAPIENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false



# System deps:
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR /code
COPY poetry.lock pyproject.toml /code/

# Project initialization:
# RUN echo "$FastAPIENV" && poetry version \
#     && poetry install \
#     $(if [ "$FastAPIENV" = 'production' ]; then echo '--no-dev'; fi) \
#     --no-interaction --no-ansi

RUN poetry install --no-interaction --no-ansi

# RUN poetry install

# Creating folders, and files for a project:
COPY . /code
CMD ["uvicorn", "backend.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--reload"]

EXPOSE 8080
