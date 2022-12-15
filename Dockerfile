FROM python:3.8
LABEL maintainer="marcon"
COPY . /app
COPY ./openssl.cnf /etc/ssl/
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python","startup.py"]