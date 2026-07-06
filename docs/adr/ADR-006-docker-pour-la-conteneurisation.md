# ADR-006 - Docker pour la conteneurisation

## Statut

Accepté

## Date

À compléter

## Contexte

Le projet doit être reproductible sur n'importe quel environnement (local, CI/CD) et orchestrer plusieurs services : API, PostgreSQL, Redis, Prometheus et Grafana.

## Décision

Utiliser **Docker et Docker Compose** pour l'orchestration locale de l'infrastructure.

## Justification

- Environnements reproductibles avec une seule commande (`docker compose up -d`)
- Isolation des services (API, base de données, cache, monitoring)
- Le monitoring (Prometheus/Grafana) est packagé dans un fichier Compose séparé (`docker-compose.monitoring.yml`), activable indépendamment

## Conséquences

- Docker Desktop est un prérequis pour le développement local
- Les migrations de schéma doivent être rejouées après un `docker compose down -v` (perte du volume de données)
- Le dashboard Grafana **Order API - Overview** est auto-provisionné au démarrage
