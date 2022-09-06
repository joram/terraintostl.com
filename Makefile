install:
	apt-get install \
		libeigen3-dev \
		libgmp-dev \
		libgmpxx4ldbl \
		libmpfr-dev \
		libboost-dev \
		libboost-thread-dev \
		libtbb-dev \
		python3-dev \
		gdal

deploy:
	cd web_app; npm run build
	aws s3 sync ./web_app/build/ s3://terraintostl.com/
	aws cloudfront create-invalidation --distribution-id=E23GF0NWEKO4ST --paths=/index.html
