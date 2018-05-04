FROM python
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y apt-utils libgphoto2-dev
#CMD [ "pip", "install", "gphoto2==1.3.1" ]
RUN pip install gphoto2
CMD ["ls"]
CMD ["python", "app.py"]