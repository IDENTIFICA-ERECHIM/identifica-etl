#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/../.."

if [ ! -d ".venv" ]; then
    echo "venv nao detectado. Criando venv..."
    python3 -m venv .venv
    echo "venv criado."
fi

echo "Ativando ambiente..."
source .venv/bin/activate
echo "Ambiente Ativado."

echo "Instalando e atualizando dependencias..."
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencias instaladas"
