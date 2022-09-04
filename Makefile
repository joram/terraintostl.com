install:
	apt-get install -y \
		libeigen3-dev \
		libgmp-dev \
		libgmpxx4ldbl \
		libmpfr-dev \
		libboost-dev \
		libboost-thread-dev \
		libtbb-dev \
		python3-dev \
		libgdal-dev \
		gdal-bin

install-mac:
	brew install gdal --HEAD

image:
	docker build . -t terrain_viewer

run:
	docker run --rm -p 3000:3000 -p 8000:8000 --name terrain_viewer terrain_viewer
