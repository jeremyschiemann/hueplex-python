FROM python:3.11-buster

RUN pip install poetry

WORKDIR ./app

COPY pyproject.toml poetry.lock action_config.yaml ./
ADD hueplex ./hueplex

RUN poetry install

CMD poetry run uvicorn hueplex.server:app --host 0.0.0.0 --port 5000