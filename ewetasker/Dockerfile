FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt

ADD . /usr/src/app
RUN openssl genrsa -out ewetasker.pem 2048
CMD ["python", "app.py"]
