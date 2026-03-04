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

- Triage par spécialisation et heure de disponibilité

- Calcul du temps moyen d'attente

- Utilisation en parrallèle de l'équippement via la capacité

- triage des equipements par heure de début (afin de traiter au plus vite les STAT)

- Mise en place de la maintenance

- Mise en place naïve de la pause déjeuner

## Stratégies

- Le scheduler teste chaque combinaison possible de techniciens spécialisés et d'équipements compatibles pour chaque échantillon

- Mise en évidence de la priorité 'STAT' lors du moment de pause

- Utilisation de la capacité pour faire en parrallèle sur un équipement

## Export et Analyse des Résultats

Le scheduler génère un rapport de détaillé. Vous pouvez rediriger la sortie pour analyser les indicateurs clés :

```bash
poetry run python3 -m lab_planner.main > rapport_planning.txt
```

## Avancement futur

- Faire une version plus intelligente de la pause déjeuner

- Intégration de metrics en incorporant le coefficient

- Intégration du nettoyage des équipements

- Intégration dans la sortie des actions (pause déjeuner sauté et netoyage)