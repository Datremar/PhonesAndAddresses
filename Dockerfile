FROM python:3.10

WORKDIR /phones-addresses

COPY /requirements.txt .
COPY ./src ./src

RUN pip install -r requirements.txt

EXPOSE 8000/tcp
EXPOSE 6379/tcp

CMD ["python", "./src/main.py"]