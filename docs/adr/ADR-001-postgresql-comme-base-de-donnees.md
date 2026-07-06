# ADR-001 - PostgreSQL comme base de données

## Statut

Accepté

## Date

À compléter (Sprint 1)

## Contexte

Le projet nécessite une base de données relationnelle pour gérer des entités fortement liées entre elles (utilisateurs, clients, produits, commandes, factures) avec des contraintes d'intégrité référentielle strictes, notamment pour la gestion des stocks et l'idempotence des paiements.

## Décision

Utiliser **PostgreSQL 15** comme base de données relationnelle principale, avec **SQLAlchemy 2** comme ORM et le pattern **Repository** pour isoler les requêtes SQL de la logique métier.

## Justification

- Fiabilité et transactions ACID, indispensables pour la cohérence des paiements et des stocks
- Support natif des UUID comme type de colonne
- Le pattern Repository isole les requêtes SQL : si le moteur de base de données change, seule la couche Repository est affectée
- Alembic assure le versioning et le rollback des migrations de schéma

## Conséquences

- Le projet dépend d'une instance PostgreSQL disponible (via Docker Compose en local)
- Toute évolution du schéma passe par une migration Alembic versionnée
- Le couplage à SQLAlchemy impose de respecter ses contraintes en mode asynchrone (voir ADR-005)
