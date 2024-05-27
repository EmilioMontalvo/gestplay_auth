FROM python:3.12.3-alpine3.20

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt

COPY ./src /code/src

CMD ["python", "src/main.py"]

