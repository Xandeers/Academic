#!/bin/bash 

echo "==== Clean de la bd ==== "
sudo docker-compose down -v 

echo "==== Lancement des conteneur ==== "
sudo docker-compose up --build