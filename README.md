# Lab Planner

## Objectif

e logiciel Lab Planner est un scheduler d’analyses de laboratoire médical.

Son objectif principal est de :

1. Organiser les échantillons (sang, urine, etc.) en fonction de leur niveau de priorité :

    - STAT : urgence vitale

    - URGENT : important mais pas critique

    - ROUTINE : analyse standard

2. Assigner intelligemment les ressources : techniciens et équipements compatibles, sans conflit d’horaires.

3. Planifier chronologiquement les analyses afin que chaque échantillon soit traité dans les délais.

4. Fournir des métriques de qualité : temps total, efficacité d’utilisation des ressources, nombre de conflits.

5. Le logiciel est conçu pour automatiser et simplifier la planification du laboratoire, tout en respectant les priorités et les disponibilités.

## Installation

Installer les dépendances avec Poetry :

```bash
poetry install
```

## Exécution

```bash
poetry run python3 -m lab_planner.mai
```

## Tests

Avec pytest :

```bash
poetry run pytest
```

ou utilisation du script :

```bash
sh run_tests.sh
```

## Evolution depuis la version SIMPLE

- a venir