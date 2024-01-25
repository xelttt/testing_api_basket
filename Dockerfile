FROM python:3.11
WORKDIR /var/tests
COPY requirements.txt /var/tests/
RUN pip install -r requirements.txt