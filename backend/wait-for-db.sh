#!/bin/bash

export PGPASSWORD="password"  # match POSTGRES_PASSWORD in docker-compose

until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for postgres at db:5432..."
  sleep 2
done

echo "Postgres is ready, starting the app..."
exec "$@"
