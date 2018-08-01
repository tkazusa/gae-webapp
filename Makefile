APP := webapp
DOCKER_IMAGE_NAME := titanic_webapp
CONTAINER_NAME := titanic_webapp


# main commands
build: Dockerfile
	docker build . -t $(DOCKER_IMAGE_NAME)

install: requirements.txt
	pip install -r requirements.txt

run: 
	docker run -itd -P --name $(CONTAINER_NAME) $(DOCKER_IMAGE_NAME)
