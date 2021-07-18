# stage 1: build
FROM python:3.9 AS builder
ADD requirements.txt /app/
RUN pip wheel --no-cache-dir -r /app/requirements.txt -w /wheels


# stage 2: run 
FROM python:3.9-slim

COPY --from=builder /wheels /wheels
RUN pip install wheels/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /runtime/
COPY . .
RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python3", "run.py" ]