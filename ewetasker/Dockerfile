FROM python:3

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt

ADD . /usr/src/app

CMD ["python", "app.py"]
