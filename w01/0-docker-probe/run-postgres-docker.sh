#!/bin/bash


sudo docker run -it --rm \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(readlink -f ../..)/data/ny_taxi_pg_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --name pg-test \
    postgres:latest

