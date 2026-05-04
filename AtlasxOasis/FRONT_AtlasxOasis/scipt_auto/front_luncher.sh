#!/bin/bash 

echo "--- build de l'image ---"
docker build -t front ../

echo "--- check nettoyage ---"

docker stop front-container 2>/dev/null || true
docker rm front-container 2>/dev/null || true

echo "--- nouveau conteneur http://localhost:8080 ---"

docker run -d -p 8080:80 --name front-container front

echo "Déploiement terminé au TOP chef !"


