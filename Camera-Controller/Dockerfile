FROM python
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y apt-utils libgphoto2-dev

RUN echo "deb-src http://archive.raspbian.org/raspbian/ jessie main contrib non-free rpi" >> /etc/apt/sources.list
RUN apt-get update

RUN apt-get build-dep -y python-imaging
RUN cat /etc/apt/sources.list
RUN apt-get install -y libjpeg62-turbo libjpeg62-turbo-dev
RUN pip install Pillow

#RUN apt-get update && apt-get install -y \
#        python-dev python-pip python-setuptools \
#        libffi-dev libxml2-dev libxslt1-dev \
#        libtiff5-dev libjpeg62-turbo-dev zlib1g-dev libfreetype6-dev \
#        liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk
## Add the dependencies to the container and install the python dependencies
#ADD requirements.txt /tmp/requirements.txt
#RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
#RUN pip install Pillow

RUN pip install -r requirements.txt
CMD ["python", "app.py"]