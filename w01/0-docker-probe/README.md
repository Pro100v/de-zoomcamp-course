# DOCKER-PROBE


## Postgres cmd 

This is command line for running Postgres into docker 

```bash
sudo docker run -it --rm \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(readlink -f ../..)/data/ny_taxi_pg_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:latest
```

## pgcli tool

To install `pgcli` run next command:

```bash
pip install pgcli
```

To run `pgcli` you should run next command: 
```bash
python -m pgcli -v
```

To run tool in any places on your PC you should install `pgcli` as **rmp** package like this command
```bash
sudo dnf install pgcli
```

> in my case, I used both way to correct install `pgcli` as rpm package


Example of command with connection to local db 
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
