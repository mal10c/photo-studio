FROM phusion/baseimage:0.10.1
CMD ["/sbin/my_init"]
ADD . /code
WORKDIR /code


RUN apt-get update
RUN apt-get install -y $(cat aptinstall.txt | tr '\n' ' ')
RUN rm -f /usr/bin/python
RUN ln -s /usr/bin/python2.7 /usr/bin/python



RUN cd dlib ; python setup.py install

#RUN pip2.7 install --upgrade pip 
#RUN pip2.7 install -r requirements.txt

#CMD ["python", "app.py"]

