FROM python:3.11-bullseye

ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install poetry

WORKDIR ./app
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-linux-x64
COPY pyproject.toml poetry.lock ./
RUN poetry install

COPY action_config.yaml tailwind.config.js ./
COPY hueplex ./hueplex
COPY static ./static
COPY templates ./templates

RUN chmod +x ./tailwindcss-linux-x64 && ./tailwindcss-linux-x64 -i ./static/input.css -o ./static/output.css && rm ./tailwindcss-linux-x64 && rm ./static/input.css

CMD uvicorn hueplex.server:app --host 0.0.0.0 --port 5000