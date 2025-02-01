#! /bin/sh

read -p "Message: " msg

docker exec -it backend-web-1 alembic revision --autogenerate -m "$msg"
docker exec -it backend-web-1 alembic upgrade head