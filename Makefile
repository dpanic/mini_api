build:
	DOCKER_BUILDKIT=1 docker \
		build \
		-t app \
		. -f ./docker/Dockerfile

stop:
	docker stop container1 || echo "no running container present"

clean:
	docker rm container1 || echo "no container present"

run: clean
	docker run -p 5000:5000 \
		--name container1 \
		-it app
