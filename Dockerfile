FROM nikolaik/python-nodejs:python3.10-nodejs18-bullseye

RUN apt update \
 && apt install -y \
  build-essential \
  libeigen3-dev \
  libgmp-dev \
  libgmpxx4ldbl \
  libmpfr-dev \
  libboost-dev \
  libboost-thread-dev \
  libtbb-dev \
  python3-dev \
  libgdal-dev \
  gdal-bin \
  python3-gdal

#ADD . /app

ADD setup.py /app/
ADD web_app/package*.json /app/web_app/

WORKDIR /app

RUN python -V

# gdal==3.0.4 requires setuptools==57.5.0
# gdal requires numpy to be installed first so that it can detect and build extensions
RUN pip install setuptools==57.5.0 \
 && pip install numpy \
 && pip install .

RUN cd web_app \
 && npm install

ADD . /app

# web_app: 3000, server/main.py: 8000
EXPOSE 3000 8000
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python3", "server/main.py"]
