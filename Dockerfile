FROM python:3.7.8-alpine3.12
RUN apk add --no-cache gcc musl-dev mariadb-dev tzdata
COPY requirements.txt /app/requirements.txt
WORKDIR /app
COPY python-api.py .
RUN pip install -r requirements.txt
EXPOSE 9000
CMD python ./python-api.py
