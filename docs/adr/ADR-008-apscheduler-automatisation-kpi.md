# ADR-008 - APScheduler pour l'automatisation des rapports KPI

## Statut

Proposé (Roadmap - EPIC 4)

## Date

À compléter

## Contexte

Le calcul des KPI quotidiens (nombre de commandes, délai moyen de paiement, taux d'erreur) doit s'exécuter automatiquement chaque jour, sans intervention manuelle, et rester intégré au processus FastAPI existant plutôt que de dépendre d'un orchestrateur externe.

## Décision

Intégrer **APScheduler** directement dans l'application FastAPI pour planifier l'exécution quotidienne (06h00) du script `scripts/kpi_report.py`.

## Justification

- Évite d'introduire un orchestrateur externe (cron système, Airflow) pour un besoin simple de planification
- S'intègre nativement au cycle de vie de l'application FastAPI (`app/main.py` ou `app/core/scheduler.py`)
- Le script génère un export CSV (`reports/kpi_YYYY-MM-DD.csv`) et doit être idempotent (une deuxième exécution le même jour écrase le fichier existant sans erreur, US-AC6)

## Conséquences

- `APScheduler` doit être ajouté à `requirements.txt`
- Le job planifié doit être couvert par des tests dédiés (`tests/test_scheduler.py`)
- Cette décision n'est pas encore implémentée à ce stade (voir [Project Charter](../gouvernance/project_character.md))
