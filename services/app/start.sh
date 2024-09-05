#!/bin/sh

set -e

echo "run db migration"
/app/migrate -path /app/migrations/main -database "$DATABASE_URL" -verbose up
/app/server