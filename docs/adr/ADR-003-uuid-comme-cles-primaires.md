# ADR-003 - UUID comme clés primaires

## Statut

Accepté

## Date

À compléter (Sprint 1)

## Contexte

Les clés primaires auto-incrémentées (entiers) nécessitent une requête à la base de données pour connaître l'identifiant d'un nouvel enregistrement, ce qui pose problème pour l'idempotence des paiements où l'identifiant doit pouvoir être connu avant la persistance.

## Décision

Toutes les clés primaires sont des **UUID générés côté application** (Python), et non des entiers auto-incrémentés.

## Justification

- Permet de générer un identifiant sans interroger la base de données au préalable, essentiel pour l'idempotence des paiements
- Évite l'exposition d'identifiants séquentiels prévisibles

## Conséquences

- Léger surcoût de stockage et d'indexation par rapport à des entiers
- Amélioration identifiée pour les sprints futurs : migrer vers **UUIDv7** (triable dans le temps) pour de meilleures performances d'index à grande échelle
