# Journal des modifications

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Le format est basé sur [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
et ce projet respecte le [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> ⚠️ **Note de réconciliation des sources** : le DEVLOG organise l'historique technique par "Sprint 1 à 4" (conception initiale → séparation Customers/Users → migration async → tests async) - ces sprints sont **déjà réalisés** et correspondent aux versions `v0.2.0`/`v0.3.0` ci-dessous. Le backlog v0.3.0 définit séparément un **nouveau** plan "Sprint 1 à 4" (à venir, sur 4 semaines) pour les fonctionnalités listées dans la section [Non publié] plus bas ; le backlog ne précise pas quel numéro de version ce plan doit produire, ce numéro n'est donc pas indiqué ici. Ces deux numérotations de sprints (l'une passée, l'autre à venir) ne se recouvrent pas et ne doivent pas être confondues.
>
> ✅ **Vérification par `git log`** : le backlog v0.3.0 indiquait le rôle `manager` comme "Fait" en v0.3.0. L'historique des commits (`git log --oneline --all -i --grep="role"`, `git log --oneline --all -- app/core/auth.py`) ne montre aucune trace de `manager`/`operator`/`viewer` dans le code - seuls `role` (générique) et `admin` y apparaissent. Ces trois rôles sont donc reclassés en Roadmap ci-dessous.
>
> 📅 **Dates** : issues de `git log --pretty=format:"%h %ad %s" --date=short` sur les commits de bump de version (`3cf6d35`, `5146b5b`) et sur le premier commit du dépôt (`25ae73a`) ainsi que le dernier commit de documentation (`ffed6bc`).

---

## [Non publié] - Sprints à venir

Backlog détaillé (EPICs, user stories, critères d'acceptation) : voir [`docs/order-api-project-documentation.pdf`](docs/order-api-project-documentation.pdf).

### À faire
- Finaliser les routes admin `GET /admin/orders` et `GET /admin/users` (EPIC 1, en cours)
- Rôles RBAC `manager`, `operator`, `viewer` - mentionnés dans le backlog, absents du code à ce jour (voir [Personas](docs/product/personas.md))
- EPIC 2 - Exports CSV/Excel : commandes, produits, utilisateurs (CSV), factures (Excel), filtre par plage de dates
- EPIC 3 - Dashboards Grafana métier : commandes/jour, temps de traitement moyen, alerte taux d'erreur (> 5%), chiffre d'affaires/jour
- EPIC 4 - Automatisation KPI : script `kpi_report.py`, exécution planifiée via APScheduler, stockage historique des KPI

---

## [v0.3.0] - 2026-05-23 → 2026-05-28

> Bump de version : commit `5146b5b` (2026-05-23). Dernière mise à jour documentaire de cette version : commit `ffed6bc` (2026-05-28).

### Ajouté
- RBAC : rôle `admin` complet (`require_role()`, commit `6a097fc` ; vérification admin `d2a7f30`)
- Table `customers` dédiée aux acheteurs externes, avec modèle, schémas, service et endpoints CRUD, et FK UUID vers `orders` et `invoices`
- Gestion de stock : colonnes `stock_quantity` et `reserved_quantity` sur `products`, décrément au paiement confirmé
- Rate limiting Redis par IP et par famille de routes
- Middleware d'audit (écrit `audit_log.csv`)
- Migration complète de la stack vers l'asynchrone : `AsyncSession`, `create_async_engine`, `lazy='selectin'` sur toutes les relations (14 fichiers migrés)
- Migration de la suite de tests vers `AsyncClient` (httpx) + `aiosqlite` + `pytest-asyncio`

### Corrigé
- `orders.customer_id` : passage d'un `String` libre sans intégrité référentielle à une `UUID FK` vers `customers.id`, avec contrainte nommée explicitement (`fk_orders_customer_id`)
- Ajout de `lazy='selectin'` sur toutes les relations SQLAlchemy pour éviter l'erreur `MissingGreenlet` en contexte async
- Détection automatique du driver de base de données pour ajouter le préfixe async approprié (`sqlite+aiosqlite://` ou `postgresql+psycopg://`), y compris en CI GitHub Actions

### Dépendances
- Ajout explicite de `greenlet` à `requirements.txt` (non fourni par défaut à partir de Python 3.14)

### Résultat
- 25/25 tests passants localement et en CI (auth, orders, products, invoices, customers)

---

## [v0.2.0] - 2026-04-01

> Bump de version : commit `3cf6d35` (2026-04-01).

### Ajouté
- Authentification : register, login, logout, refresh (tokens JWT access + refresh)
- Endpoint `users/me` (profil de l'utilisateur connecté)
- Paiement idempotent via `Idempotency-Key` (cache Redis)
- Facturation automatique à chaque paiement réussi
- Exposition Prometheus `/metrics` (`http_requests_total` + histogramme de durée)
- Dashboard Grafana technique (latence p95, RPS, taux d'erreur)

---

## Version initiale - Conception (pré-v0.2.0) - depuis 2026-03-06

> Premier commit : `25ae73a` (2026-03-06).

### Ajouté
- Architecture initiale du back-office headless : FastAPI, PostgreSQL, Redis
- Architecture en couches `Endpoint → Service → Repository → Database`
- Clés primaires UUID générées côté application
- Alembic pour le versioning des migrations de schéma
