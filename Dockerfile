FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /task_t
WORKDIR /task_t
COPY req.txt /task_t/
RUN pip install -r req.txt
COPY . /task_t/