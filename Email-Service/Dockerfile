FROM resin/raspberrypi3-python:3.6
ADD . /share
WORKDIR /share
RUN pip install -r requirements.txt
CMD ["python", "-u", "app.py"]
