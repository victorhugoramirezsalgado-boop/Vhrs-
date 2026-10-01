name: Diagnostico de archivos corruptos

on:
  workflow_dispatch:

jobs:
  revisar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Ejecutar diagnostico
        run: python detectar_corrupcion.py
