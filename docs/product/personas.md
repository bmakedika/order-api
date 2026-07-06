# Personas

Trois profils utilisateurs ont été identifiés comme cibles principales de la plateforme (source : backlog v0.3.0). Chaque profil a des besoins, des contraintes et un niveau de maîtrise technique différent.

---

## Persona 1 - Le fondateur de PME e-commerce

**Profil** : dirige une boutique en ligne de 10 à 50 commandes par jour. Non technique.

**Besoin** : suivre les commandes et les paiements sans dépendre d'un développeur pour chaque export de données.

**Frustration actuelle** : Shopify lui coûte cher en abonnement et en apps tierces, et il ne peut pas accéder librement à ses données brutes.

**Ce qu'il attend** : un backoffice simple, des exports CSV en un clic, des dashboards lisibles sans formation.

---

## Persona 2 - Le responsable opérationnel

**Profil** : gère une équipe de 3 à 10 personnes (commerciaux, logistique). Maîtrise d'Excel, pas de code.

**Besoin** : visualiser les commandes en cours, suivre les expéditions, détecter les incidents en temps réel.

**Frustration actuelle** : les outils existants mélangent tout ; il doit naviguer entre plusieurs onglets pour avoir une vue complète de l'activité.

**Ce qu'il attend** : un dashboard unifié avec accès sécurisé par rôle, et des alertes automatiques en cas d'anomalie.

---

## Persona 3 - Le développeur intégrateur

**Profil** : développeur freelance ou en agence, chargé d'intégrer un backend e-commerce pour un client PME.

**Besoin** : une API bien documentée, des endpoints stables, une authentification robuste et une architecture extensible.

**Frustration actuelle** : les solutions SaaS imposées n'exposent pas de vraie API REST, ou le font de manière partielle et mal documentée.

**Ce qu'il attend** : un projet open source, bien structuré, avec documentation Swagger automatique et tests couvrant les cas critiques.

---

## Rôles et permissions (RBAC)

| Rôle | Profil | Permissions | Implémenté |
|---|---|---|---|
| `user` | Client | Passer des commandes, consulter ses propres commandes et factures | v0.2.0 |
| `admin` | Administrateur | Gérer le catalogue, exporter les données, accéder aux dashboards, superviser l'ensemble de l'activité | v0.3.0 |
| `manager` | Équipe métier | Gérer le catalogue produit, les prix et le stock. Accès aux exports de données et aux KPI métier | Roadmap |
| `operator` (Commercial) | Équipe métier | Consulter les commandes, suivre les paiements, analyser la performance commerciale | Roadmap |
| `viewer` (Opérationnel) | Équipe métier / exploitation | Superviser les métriques, surveiller les incidents, accéder aux dashboards temps réel | Roadmap |

Le système `require_role()` (`app/core/auth.py`, commit `6a097fc`) est une factory générique conçue pour accueillir n'importe quel rôle. Seuls `user` (`64b795f`, `d2a7f30`) et `admin` (`d2a7f30`) sont, à ce jour, réellement câblés dans le code.

> ✅ **Incohérence résolue via `git log`** : le backlog v0.3.0 (section 4) marquait `manager` comme "Fait" en v0.3.0. Vérification par l'historique des commits (`git log --oneline --all -i --grep="role"` et `git log --oneline --all -- app/core/auth.py`) : aucun commit n'introduit ou ne modifie la valeur `manager` (ni `operator`/`viewer`) dans le code. Seuls `role` (générique, `64b795f`) et la vérification du rôle `admin` (`d2a7f30`) apparaissent. `manager`, `operator` et `viewer` sont donc au stade **Roadmap uniquement** - mentionnés dans le backlog mais absents du code à ce jour.
