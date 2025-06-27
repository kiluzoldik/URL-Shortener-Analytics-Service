DC = docker compose
EXEC = docker exec -it
APP_FILE = docker_compose/app.yml
STORAGES_FILE = docker_compose/storages.yml
CACHE_FILE = docker_compose/redis.yml
DB_CONTAINER = docker_compose-shortener_storage-1
ENV_FILE = --env-file ../URL-Shortener-Analytics-Service/.env
APP_CONTAINER = docker_compose-shortener_service-1
LOGS = docker logs

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

.PHONY: cache
cache:
	${DC} -f ${CACHE_FILE} ${ENV_FILE} up -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: postgres
postgres:
	${EXEC} ${DB_CONTAINER} psql -U postgres -d shortener_db

.PHONY: storages-logs
storages-logs:
	${LOGS} ${DB_CONTAINER} -f

.PHONY: app
app:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} ${ENV_FILE} up -d --force-recreate --build

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} down

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: revision
revision:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} exec shortener_service alembic revision --autogenerate -m ''

.PHONY: migration
migration:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} exec shortener_service alembic upgrade head

.PHONY: downgrade
downgrade:
	${DC} -f ${APP_FILE} -f ${STORAGES_FILE} exec shortener_service alembic downgrade base