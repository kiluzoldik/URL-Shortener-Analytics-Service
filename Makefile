DC = docker compose
EXEC = docker exec -it
APP_FILE = docker_compose/app.yml
STORAGES_FILE = docker_compose/storages.yml
DB_CONTAINER = shortener_storage
ENV_FILE = --env-file ../URL-Shortener-Analytics-Service/.env
APP_CONTAINER = docker_compose-shortener_service-1
LOGS = docker logs

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV_FILE} up -d

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