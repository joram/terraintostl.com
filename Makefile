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

deploy_web:
	cd web_app; npm run build
	aws s3 sync ./web_app/build/ s3://terraintostl.com/
	aws cloudfront create-invalidation --distribution-id=E23GF0NWEKO4ST --paths=/index.html

deploy_server:
	cd server; docker build -t joram87/terraintostl .
	docker push joram87/terraintostl
	ssh 192.168.1.222 "cd projects/nas; docker-compose pull terraintostl; docker-compose up -d terraintostl; docker-compose logs -f terraintostl"

tail_logs:
	ssh 192.168.1.222 "cd projects/nas; docker-compose logs -f terraintostl"

