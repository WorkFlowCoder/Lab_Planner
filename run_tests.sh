#!/bin/bash

# Ajouter le dossier courant au PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Lancer les tests avec Poetry
poetry run pytest
