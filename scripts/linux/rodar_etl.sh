#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."

if [ ! -d ".venv" ]; then
    echo "Ambiente virtual (.venv) nao detectado."
    echo "Rode o script 'setup.sh' para criar o ambiente."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "Arquivo .env nao encontrado."
    exit 1
fi

source .venv/bin/activate
python -m db.atualizar_db "$@"
