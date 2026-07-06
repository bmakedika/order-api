# ADR-004 - Redis comme cache multi-usages

## Statut

Accepté

## Date

À compléter (Sprint 1)

## Contexte

Plusieurs besoins transverses nécessitent un stockage rapide et temporaire indépendant de la base de données relationnelle : idempotence des paiements, invalidation des tokens JWT (blacklist), et limitation du nombre de requêtes (rate limiting).

## Décision

Utiliser **Redis 7** comme cache multi-usages pour ces trois besoins.

## Justification

- Idempotence des paiements : la clé `Idempotency-Key` est mise en cache 24h pour garantir qu'aucun double paiement n'est possible
- Blacklist des tokens JWT révoqués, sans dépendre d'une table dédiée en base
- Rate limiting par IP et par groupe de routes
- Redis est adapté à des données volatiles et à durée de vie courte, contrairement à PostgreSQL

## Conséquences

- Ajoute une dépendance d'infrastructure supplémentaire (conteneur Redis en local via Docker Compose)
- La perte du cache Redis (redémarrage sans persistance) réinitialise la fenêtre d'idempotence et la blacklist des tokens, ce qui doit être pris en compte en production
