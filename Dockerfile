FROM python:3.8
LABEL maintainer="marcon"
WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

COPY . .
COPY ./openssl.cnf /etc/ssl/

CMD ["python","startup.py"]