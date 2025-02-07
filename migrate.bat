set /P message="Eingabe: "
docker compose exec web alembic revision --autogenerate -m "%message%"
docker compose exec web alembic upgrade head