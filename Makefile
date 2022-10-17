install:
	apt-get install \
		binutils \
		libproj-dev \
		gdal-bin


build:
	cd server; docker build -t joram87/terraintostl .

bash: build
	docker run -it -v ${PWD}/data:/data -v ${PWD}/stls:/stls -v ${PWD}/server:/app joram87/terraintostl bash

reduce: build
	docker run -it -v ${PWD}/data:/data -v ${PWD}/stls:/stls joram87/terraintostl python ./stl_generator/stl_util.py

deploy_web:
	cd web_app; npm run build
	aws s3 sync ./web_app/build/ s3://terraintostl.com/
	aws cloudfront create-invalidation --distribution-id=E23GF0NWEKO4ST --paths=/index.html

deploy_server: build
	docker push joram87/terraintostl
	ssh 192.168.1.222 "cd projects/nas; docker-compose pull terraintostl; docker-compose up -d terraintostl; docker-compose logs -f terraintostl"

tail_logs:
	ssh 192.168.1.222 "cd projects/nas; docker-compose logs -f terraintostl"

