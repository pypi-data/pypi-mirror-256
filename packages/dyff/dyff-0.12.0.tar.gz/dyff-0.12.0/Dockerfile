ARG CONTAINER_PROXY
FROM ${CONTAINER_PROXY}python:3.9-bullseye AS build

ENV PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1"

WORKDIR /build/

# hadolint ignore=DL3013,DL3042
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt ./

# hadolint ignore=DL3013,DL3042
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install -r requirements.txt

COPY . ./

RUN mv pyproject.api.toml pyproject.toml

# hadolint ignore=DL3013,DL3042
RUN --mount=type=cache,target=/root/.cache \
    python3 -m pip install .

ARG CONTAINER_PROXY
FROM ${CONTAINER_PROXY}python:3.9-slim-bullseye

COPY --from=build /usr/local/ /usr/local/

ENV PYTHONDONTWRITEBYTECODE="1" \
    PYTHONUNBUFFERED="1"

ENTRYPOINT ["uvicorn", "dyff.api.server:app", "--proxy-headers", "--host", "0.0.0.0"]
