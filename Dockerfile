FROM ubuntu:20.04
FROM python:3.8

RUN mkdir lab3
COPY . /lab3
WORKDIR lab3
RUN pip install -r requirements.txt
EXPOSE 8000 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
