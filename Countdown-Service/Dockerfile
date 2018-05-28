FROM resin/raspberry-pi-alpine-python:latest
ADD . /share
WORKDIR /share
RUN pip install -r requirements.txt
CMD ["python", "-u", "app.py"]
