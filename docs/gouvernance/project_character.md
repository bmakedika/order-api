# Project Charter

## Nom du projet

Order API - Backoffice et API REST headless de gestion e-commerce sécurisé

## Contexte

Les PME qui lancent leur e-commerce n'ont pas toujours les ressources pour développer un système sur mesure. Elles se tournent vers des solutions clés en main (Shopify, WooCommerce, PrestaShop) pour leur rapidité de mise en place, mais ces outils atteignent rapidement leurs limites dès que l'entreprise veut adapter la plateforme à ses processus spécifiques, connecter des outils tiers ou exploiter finement ses données métier.

Cette dépendance entraîne trois problèmes concrets :

- **Rigidité technique** : impossible d'adapter les flux métier sans passer par un développeur et payer des frais de personnalisation élevés
- **Perte de souveraineté sur les données** : les données clients, commandes et performances sont hébergées chez un tiers, sans accès direct ni export structuré
- **Absence de pilotage métier** : sans dashboards ni exports automatisés, les équipes prennent des décisions à l'aveugle, sans indicateurs fiables ni temps réel

Order API n'est pas une alternative à Shopify pour vendre en ligne : c'est un système de gestion opérationnelle et analytique headless API-first, destiné aux équipes qui ont besoin de contrôle, de flexibilité et d'accès direct à leurs données métier.

## Vision

Permettre aux entreprises de faire évoluer leur e-commerce librement, sans dépendre en permanence de développeurs, tout en restant pleinement souveraines sur leurs données - la flexibilité du sur-mesure, sans la complexité technique qui va avec.

## Objectifs métiers

- Fournir une gestion complète du cycle de vie des commandes (brouillon → articles → paiement → livraison)
- Garantir l'intégrité des stocks (réservation puis décrément uniquement à la confirmation du paiement)
- Assurer la traçabilité des paiements et de la facturation
- Sécuriser l'accès aux données par un contrôle des rôles fin (RBAC), avec accès direct et adapté aux données métier pour les administrateurs, commerciaux et opérationnels
- Donner aux administrateurs un accès en libre-service aux exports de données (CSV/Excel) - *Roadmap*
- Fournir des tableaux de bord métier en temps réel - *Roadmap*
- Automatiser les rapports KPI périodiques via des scripts planifiés - *Roadmap*

## Objectifs techniques

- Construire une API headless et API-first, connectable à n'importe quel frontend
- Adopter une architecture en couches claire (Endpoint → Service → Repository)
- Garantir l'idempotence des paiements
- Fournir une observabilité native (Prometheus / Grafana)
- Automatiser les tests et l'intégration continue (CI/CD)
- Mettre en place un pipeline de données automatisé (collecte, transformation, stockage) - *Roadmap*

## Périmètre actuel - état au 20/06/2026 (base v0.3.0)

| Fonctionnalité | État | Version | Notes |
|---|---|---|---|
| Auth (register, login, logout, refresh) | ✅ Fait | v0.2.0 | Tokens JWT accès + refresh |
| `users/me` | ✅ Fait | v0.2.0 | Profil de l'utilisateur connecté |
| RBAC `require_role()` + filtrage ownership | ✅ Fait | v0.3.0 | Orders et invoices filtrés par utilisateur |
| CRUD Produits | ✅ Fait | - | GET/POST/PUT/DELETE |
| Commandes (création, articles, paiement, statut) | ✅ Fait | - | Filtrées par utilisateur authentifié (ownership) |
| Factures | ✅ Fait | - | Créées automatiquement après paiement |
| Paiement idempotent | ✅ Fait | - | `Idempotency-Key` (Redis) |
| Rate limiting (Redis) | ✅ Fait | - | Par IP et par famille de routes |
| Middleware d'audit | ✅ Fait | - | Écrit `audit_log.csv` |
| Prometheus `/metrics` | ✅ Fait | - | `http_requests_total` + histogramme de durée |
| Dashboard Grafana (technique) | ✅ Fait | - | Latence p95, RPS, taux d'erreur |
| Tests | ✅ Fait | - | 25 tests pytest async (auth, orders, products, invoices, customers) |
| Séparation Customers / Users | ✅ Fait | v0.3.0 | Table `customers`, FK UUID vers `orders` et `invoices` |
| Gestion de stock (réservation) | ✅ Fait | v0.3.0 | `stock_quantity` / `reserved_quantity`, décrément au paiement confirmé |
| Migration stack async | ✅ Fait | v0.3.0 | `AsyncSession`, `create_async_engine`, `lazy='selectin'` - 14 fichiers migrés |
| Routes admin (`GET /admin/orders`, `/admin/users`) | 🔶 En cours | - | Sprint RBAC (T5) non terminé |
| Exports de données (CSV/Excel) | ⏳ Non commencé | - | Roadmap - Sprint Exports |
| Tableaux de bord métier (Grafana) | ⏳ Non commencé | - | Roadmap - Sprint Dashboards |
| Automatisation / scheduler KPI | ⏳ Non commencé | - | Roadmap - Sprint KPI |
| Pipeline de données (KPI, exports, dashboards) | ⏳ Non commencé | - | Structuration prévue sur les prochains sprints du backlog |

> Détail du backlog (EPICs, user stories, critères d'acceptation, planification des 4 sprints à venir) : voir [`order-api-project-documentation.pdf`](../order-api-project-documentation.pdf).

## Critères de succès

- Pipeline de tests automatisé et CI opérationnelle
- Intégrité référentielle complète (contraintes FK nommées)
- Dashboard d'observabilité accessible
- Reproductibilité de l'environnement via Docker
- Meilleure gouvernance des données : un client ne peut pas accéder aux données d'un autre utilisateur
- Efficacité opérationnelle : les administrateurs pourront exporter les données sans accès direct à la base (Roadmap)
- Visibilité métier : dashboards Grafana mettant en avant des indicateurs actionnables (Roadmap)
