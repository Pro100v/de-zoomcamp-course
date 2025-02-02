# Workflow Orchestration


For creating lab's environment, we must run 2 `docker-cmopmose.yml' files:

- `./docker/postgres/dockert-compose.yml` : run a setup from **Postgres** data base & **pgAdmin** - postgres managing tools
- `./docker/kestra/dockert-compose.yml`: run setup from **Kestra** data pipeline orchestration tool with own **Postgres** metadata base.

> It's very import what 2 docker compose files use the same network, based on `/dockers/postgres/docker-compose.yml` file network: in this file network has name `zoomcamp` while `./docker/kestra/dockert-compose.yml` the network has name `postgres_zoomcamp` and option `external: true`
