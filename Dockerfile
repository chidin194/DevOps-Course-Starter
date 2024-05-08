FROM python:latest
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH=$PATH:/root/.local/bin/
COPY . /app
WORKDIR /app
RUN poetry install
EXPOSE 5000
ENTRYPOINT poetry run flask run --host=0.0.0.0
