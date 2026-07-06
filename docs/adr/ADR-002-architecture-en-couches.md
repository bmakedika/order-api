# ADR-002 - Architecture en couches (Endpoint → Service → Repository)

## Statut

Accepté

## Date

À compléter (Sprint 1)

## Contexte

Le projet doit rester maintenable et testable à mesure que la logique métier (RBAC, gestion des stocks, idempotence des paiements) se complexifie. Sans séparation claire, la logique métier et les requêtes SQL tendent à se mélanger dans les endpoints.

## Décision

Adopter une architecture en couches strictes :

```
Endpoint → Service → Repository → Database
```

Chaque couche a une responsabilité unique.

## Justification

- Le Repository isole les requêtes SQL : si le moteur de base de données change, seule cette couche est affectée
- Le Service porte la logique métier indépendamment du framework web
- Les Endpoints ne gèrent que la validation des requêtes/réponses (Pydantic) et l'orchestration
- Facilite les tests unitaires par couche

## Conséquences

- Toute nouvelle fonctionnalité doit traverser les trois couches, ce qui augmente le nombre de fichiers à modifier pour un même changement
- Discipline requise pour ne pas court-circuiter une couche (ex. appeler directement le Repository depuis un Endpoint)
