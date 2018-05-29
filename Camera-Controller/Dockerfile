FROM python
ADD . /share
WORKDIR /share

RUN echo "deb-src http://archive.raspbian.org/raspbian/ jessie main contrib non-free rpi" >> /etc/apt/sources.list
RUN apt-get update && \
    apt-get install -y \
        apt-utils \
        libgphoto2-dev && \
    apt-get build-dep -y \
        python-imaging && \
    apt-get install -y \
        libjpeg62-turbo \
        libjpeg62-turbo-dev

RUN pip install Pillow

RUN pip install -r requirements.txt
CMD ["python", "-u", "app.py"]