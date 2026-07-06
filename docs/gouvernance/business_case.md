# Business Case

## Situation actuelle (As-Is)

```
PME  →  Solution SaaS clé en main (Shopify, WooCommerce, PrestaShop)  →  Rigidité, dépendance, absence de pilotage
```

Trois problèmes concrets découlent de cette dépendance :

- **Rigidité technique** : impossible d'adapter les flux métier sans développeur, avec des frais de personnalisation élevés
- **Perte de souveraineté sur les données** : données clients, commandes et performances hébergées chez un tiers, sans accès direct ni export structuré
- **Absence de pilotage métier** : décisions prises à l'aveugle, faute de dashboards ou d'exports automatisés

## Situation cible (To-Be)

```
PME  →  Order API (headless, self-hosted, API-first)  →  RBAC fin + exports en libre-service + dashboards métier + observabilité
```

## Positionnement concurrentiel

| Critère | Shopify | WooCommerce | Medusa.js | Sur mesure | Order API |
|---|---|---|---|---|---|
| API REST headless | Partiel | Non | Oui | Variable | Oui - natif |
| RBAC granulaire | Non | Partiel | Oui | Variable | Oui - natif |
| Exports CSV/Excel | App payante | Plugin | Partiel | À développer | Oui - Roadmap |
| Monitoring intégré | Non | Non | Partiel | À développer | Oui - natif |
| Open source | Non | Oui | Oui | Oui | Oui |
| Coût initial | Abonnement | Hébergement | Gratuit | Élevé | Gratuit |

Order API se positionne comme une alternative open source, headless et orientée données, à destination des équipes techniques et des PME qui souhaitent reprendre le contrôle sur leur infrastructure e-commerce sans les contraintes des solutions SaaS propriétaires. Ce n'est pas un concurrent frontal de Shopify pour vendre en ligne, mais un système de gestion opérationnelle et analytique.

## Bénéfices attendus

### Souveraineté des données

Les PME gardent la maîtrise de leurs données métier (commandes, clients, paiements) plutôt que de dépendre d'une plateforme tierce fermée.

### Flexibilité

Architecture API-first et headless : connexion possible à n'importe quel frontend ou outil externe, sans stack imposée.

### Fiabilité

Idempotence garantie des paiements et intégrité référentielle des commandes (aucun double paiement, aucun stock incohérent).

### Gouvernance des données

RBAC : un client ne peut pas accéder aux données d'un autre utilisateur.

### Observabilité

Dashboards Prometheus/Grafana intégrés par défaut pour le suivi opérationnel (latence p95, RPS, taux d'erreur).

### Efficacité opérationnelle et visibilité métier - *Roadmap*

Exports en libre-service (CSV/Excel) sans accès direct à la base de données, dashboards métier temps réel (commandes/jour, temps de traitement, chiffre d'affaires), et rapports KPI automatisés - ces bénéfices ne sont pas encore mesurables, les fonctionnalités correspondantes (EPIC 2, 3, 4 du backlog) n'étant pas encore implémentées.
