FROM python
ADD . /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y apt-utils libgphoto2-dev
RUN pip install -r requirements.txt
CMD ["python", "app.py"]