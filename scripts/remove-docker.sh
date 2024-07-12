ODOO_VERSION="17"
ODOO_IMAGE="odoo:$ODOO_VERSION"
POSTGRES_VERSION="16.2"
POSTGRES_IMAGE="postgres:$POSTGRES_VERSION"
PGADMIN_IMAGE="dpage/pgadmin4:latest"
NETWORK="odoo_default"

docker rm $(docker stop $(docker ps -a -q --filter "name=odoo_${ODOO_VERSION}_*" --format="{{.ID}}"))
for image in $ODOO_IMAGE $POSTGRES_IMAGE $PGADMIN_IMAGE; do
    docker rmi $(docker images -q --filter reference=$image)
done
docker volume ls --quiet --filter name="odoo_*" | grep -E "odoo_*" | awk '{ print $1 }' | xargs -r docker volume rm
docker network rm $NETWORK