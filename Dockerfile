FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /asana_taks
WORKDIR /asana_taks
COPY req.txt /asana_taks/
RUN pip install -r req.txt
COPY . /asana_taks/