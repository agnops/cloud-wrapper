FROM python:3-alpine

ENV FLASK_APP=main.py
ENV FLASK_ENV=development

COPY app/DockerOps ./DockerOps
COPY app/DnsOps ./DnsOps
COPY app/main.py .
COPY app/aws.requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade -r requirements.txt && rm requirements.txt

EXPOSE 5000

ENTRYPOINT flask run -h 0.0.0.0