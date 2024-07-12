#!/bin/bash

FILTER="odoo_*"
IMAGES=( odoo:17 postgres:16.2 dpage/pgadmin4:latest )

docker rm $(docker stop $(docker ps -a -q --filter "name=$FILTER"))
for image in ${IMAGES[@]}
do
  docker rmi $(docker images -q --filter reference=$image)
done
docker volume ls --quiet --filter "name=$FILTER" | awk '{ print $1 }' | xargs -r docker volume rm
docker network ls --quiet --filter "name=$FILTER" | awk '{  print $1 }' | xargs -r docker network rm