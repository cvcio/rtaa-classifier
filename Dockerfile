FROM python:3.8-buster AS venv

ENV POETRY_VERSION=1.1.13
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH

WORKDIR /svc
COPY ./pyproject.toml ./poetry.lock ./

RUN python -m venv --copies /svc/venv
RUN . /svc/venv/bin/activate && poetry install --no-dev

FROM python:3.8-slim as prod

COPY --from=venv /svc/venv /svc/venv/
ENV PATH /svc/venv/bin:$PATH

WORKDIR /svc

COPY .env.template /svc/.env
COPY server/ /svc/server
COPY conf/ /svc/conf
COPY models/ /svc/models

EXPOSE 50030
CMD ["python", "server/app.py"]