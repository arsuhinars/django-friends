
# Base image
FROM python:3.11-slim as base

ARG BACKEND_PORT=8000
ENV BACKEND_PORT=$BACKEND_PORT

WORKDIR /backend

# Install python packages
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv --no-cache-dir --disable-pip-version-check
RUN pipenv install --system --deploy --ignore-pipfile

# Copy sources
COPY django_friends/ django_friends/
COPY api/ api/
COPY manage.py .

# Copy entrypoint script
COPY docker-entrypoint.sh .

EXPOSE $BACKEND_PORT


# Development image
FROM base as dev

WORKDIR /backend

# Add entrypoint script
ENTRYPOINT [ "bash", "-c", "./docker-entrypoint.sh", "docker-entrypoint.sh" ]
