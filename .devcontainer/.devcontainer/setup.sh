#!/usr/bin/env bash
set -e

# Aktualizacje i podstawy
apt-get update -y && apt-get install -y git wget

# Wirtualne środowisko (opcjonalnie)
python -m venv .venv
echo 'source .venv/bin/activate' >> ~/.bashrc
source .venv/bin/activate

# Zależności
pip install --upgrade pip
pip install -r requirements.txt

# Pobranie przykładowego modelu CPU (zmień na Bielik, jeśli jest na HF)
# UWAGA: dla CPU weź mały model, żeby test nie trwał wieczność.
python - << 'PY'
print("✅ Setup completed")
PY
