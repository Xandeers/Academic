!#/bin/bash


CONTAINER_NAME="front-container"
IMAGE_NAME="front"

docker stop $CONTAINER_NAME 2>/dev/null || true

docker rm $CONTAINER_NAME 2>/dev/null || true

docker rmi $IMAGE_NAME 2>/dev/null || true

echo "Nettoyagé !"