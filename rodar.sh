#!/usr/bin/env bash
set -euo pipefail

sudo docker compose up -d mysql
sudo docker compose run --rm --build etl

echo
echo "ETL concluido. Estado do banco:"
sudo docker compose ps
