#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Erro: Python 3 não encontrado. Instale Python 3.10 ou superior."
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

mkdir -p instance/logs
echo
echo "Ambiente preparado."
echo "Para iniciar: source .venv/bin/activate && flask --app run.py run --debug"
