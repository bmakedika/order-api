# ADR-007 - openpyxl + csv pour les exports de données

## Statut

Proposé (Roadmap - EPIC 2)

## Date

À compléter

## Contexte

Les administrateurs ont besoin d'exporter les commandes, produits, utilisateurs et factures pour les analyser dans Excel/Python ou les transmettre à la comptabilité, sans accès direct à la base de données.

## Décision

Utiliser le module standard `csv` pour les exports CSV (commandes, produits, utilisateurs) et **openpyxl** pour l'export des factures au format Excel (`.xlsx`).

## Justification

- `csv` fait partie de la bibliothèque standard Python, sans dépendance supplémentaire
- `openpyxl` est nécessaire uniquement pour le format `.xlsx` attendu par la comptabilité (US8)
- Les exports restent protégés par `require_admin` et supportent un filtre optionnel par plage de dates (US9)

## Conséquences

- `openpyxl` doit être ajouté à `requirements.txt`
- Les exports doivent gérer le cas d'un jeu de données vide (fichier avec uniquement l'en-tête)
- Cette décision n'est pas encore implémentée à ce stade (voir [Project Charter](../gouvernance/project_character.md))
