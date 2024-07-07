FROM python:3.11 as base
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin/
WORKDIR /app
COPY ./poetry.toml ./pyproject.toml /app/
RUN poetry install
COPY . /app
EXPOSE 5000


FROM base as production
ENV FLASK_DEBUG=false
ENTRYPOINT poetry run flask run --host=0.0.0.0

FROM base as development
ENV FLASK_DEBUG=true
ENTRYPOINT poetry run flask run --host=0.0.0.0

