APP := webapp
DOCKER_IMAGE_NAME := titanic_webapp
CONTAINER_NAME := titanic_webapp


# main commands
build: setup-files
	docker build . -t $(DOCKER_IMAGE_NAME)

install: requirements.txt
	pip install -r requirements.txt

run: 
	docker run -d -P -p 33000:3000 --name $(CONTAINER_NAME) $(DOCKER_IMAGE_NAME) \
	python3 webapp/app.py


setup-files: Dockerfile

Dockerfile: FORCE
	cp dockerfiles/webapp/Dockerfile .

FORCE:
.PHONY: FORCE
