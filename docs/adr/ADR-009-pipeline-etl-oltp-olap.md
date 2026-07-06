# ADR-009 - Pipeline ETL léger et séparation OLTP/OLAP

## Statut

Proposé (Roadmap - EPIC 4, long terme)

## Date

À compléter

## Contexte

Au-delà de l'API transactionnelle, le projet vise à poser les bases d'une couche analytique : collecte automatisée des KPI, exports structurés et dashboards métier. Faire porter les requêtes de reporting directement sur la base transactionnelle (OLTP) risque à terme de dégrader les performances de l'API.

## Décision

Mettre en place un pipeline ETL léger (Extract-Transform-Load) pour alimenter un stockage analytique dédié (schéma `analytics` ou tables dédiées dans PostgreSQL), en vue d'une séparation simplifiée OLTP/OLAP.

## Justification

- Isole les requêtes de reporting/dashboards de la base transactionnelle qui sert l'API
- Permet de conserver un historique interrogeable des KPI calculés (US17)
- Reste volontairement "léger" : pas d'entrepôt de données dédié à ce stade, contrairement à un projet analytique pur (ex. RetailFlow/BigQuery)

## Conséquences

- Complexité supplémentaire à gérer (synchronisation entre couche transactionnelle et couche analytique)
- Décision explicitement positionnée comme un objectif à long terme dans le backlog - non détaillée davantage dans les sources fournies à ce stade
- Cette décision n'est pas encore implémentée (voir [Project Charter](../gouvernance/project_character.md))
