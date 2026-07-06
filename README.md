# Order API

[![CI](https://github.com/bmakedika/order-api/actions/workflows/ci.yml/badge.svg)](https://github.com/bmakedika/order-api/actions)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688)
![License](https://img.shields.io/badge/license-MIT-green)

## Présentation

Order API est un backoffice e-commerce sécurisé, headless et API-first, conçu pour donner aux PME de la flexibilité, de la souveraineté sur leurs données et des fonctionnalités orientées analytique

Le projet gère l'intégralité du cycle de vie d'une commande — authentification, catalogue produits, paiements idempotents sécurisés, facturation automatisée et supervision en temps réel — et reste connectable à n'importe quel frontend ou outil externe

Order API couvre l'ensemble des besoins d'un backoffice moderne :

- authentification et contrôle d'accès par rôle (RBAC)
- gestion du catalogue et des stocks
- cycle de vie complet des commandes et des paiements
- facturation automatisée
- observabilité temps réel
- exports et pilotage métier (roadmap)

---

## Contexte

Les PME qui lancent leur e-commerce n'ont pas toujours les ressources pour développer un système sur mesure. Elles se tournent vers des solutions clés en main (Shopify, WooCommerce, PrestaShop) pour leur rapidité de mise en place, mais ces outils atteignent rapidement leurs limites dès que l'entreprise veut adapter la plateforme à ses processus spécifiques, connecter des outils tiers ou exploiter finement ses données métier

Cette dépendance entraîne trois problèmes concrets :

- une rigidité technique : impossible d'adapter les flux métier sans développeur, avec des frais de personnalisation élevés
- une perte de souveraineté sur les données : données clients, commandes et performances hébergées chez un tiers, sans accès direct ni export structuré
- une absence de pilotage métier : décisions prises à l'aveugle, faute de dashboards ou d'exports automatisés

Order API est né de la volonté de répondre à ce problème par une architecture headless API-first, que les équipes techniques et les PME peuvent adapter à leurs propres processus, sans dépendre en permanence d'un éditeur tiers

---

## Vision

Permettre aux entreprises de faire évoluer leur e-commerce librement, sans dépendre en permanence de développeurs, tout en restant pleinement souveraines sur leurs données — la flexibilité du sur-mesure, sans la complexité technique qui va avec

---

## Valeur métier

### Souveraineté

Les PME gardent la maîtrise de leurs données métier (commandes, clients, paiements) plutôt que de dépendre d'une plateforme tierce fermée

### Flexibilité

Architecture API-first et headless : connexion possible à n'importe quel frontend ou outil externe, sans stack imposée

### Fiabilité

Idempotence garantie des paiements et intégrité référentielle des commandes — aucun double paiement, aucun stock incohérent

### Gouvernance

Contrôle d'accès par rôle (RBAC) : un client ne peut jamais accéder aux données d'un autre utilisateur

---

## Architecture

```
Client / Frontend  →  API FastAPI (JWT, RBAC, rate limiting)  →  Service  →  Repository (SQLAlchemy)  →  PostgreSQL
                                                                                  ↳ Redis (idempotence, blacklist JWT, rate limiting)
                                                                                  ↳ Prometheus  →  Grafana
```

---

## Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy / Alembic
- Redis
- Prometheus / Grafana
- Docker
- GitHub Actions
- openpyxl / APScheduler (roadmap)

---

## Principaux KPI

- Requêtes HTTP et latence (p95)
- Débit (RPS) et taux d'erreur technique
- Commandes par jour (roadmap)
- Temps de traitement moyen des commandes (roadmap)
- Chiffre d'affaires par jour (roadmap)

---

## Auteur

Bienvenu MAKEDIKA MAKUALA
