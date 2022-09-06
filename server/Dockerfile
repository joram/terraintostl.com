FROM andrejreznik/python-gdal:stable

ADD setup.py /app/
RUN pip install --upgrade pip
RUN pip install /app
ADD . /app

RUN mkdir /stls
RUN mkdir /data

VOLUME /stls
VOLUME /data

WORKDIR /app
CMD ["python", "-m", "main"]
