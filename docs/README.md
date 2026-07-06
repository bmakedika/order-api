# Documentation - Order API

Ce dossier contient l'ensemble de la documentation du projet, organisée en trois catégories.

---

## Gouvernance

| Fichier | Description |
|---|---|
| [`gouvernance/project_character.md`](gouvernance/project_character.md) | Project Charter : contexte, vision, objectifs et critères de succès |
| [`gouvernance/business_case.md`](gouvernance/business_case.md) | Business Case : situation actuelle, situation cible et bénéfices attendus |
| [`gouvernance/glossaire.md`](gouvernance/glossaire.md) | Glossaire des termes techniques et métier du projet |

---

## Produit

| Fichier | Description |
|---|---|
| [`product/personas.md`](product/personas.md) | Personas : profils utilisateurs et leurs objectifs |
| [`product/kpi_catalog.md`](product/kpi_catalog.md) | Catalogue des indicateurs d'observabilité et statut d'implémentation |
| [`product/data_dictionary.md`](product/data_dictionary.md) | Data Dictionary : description des entités du projet |
| [`order-api-project-documentation.pdf`](order-api-project-documentation.pdf) | Product backlog, user stories, sprint planning, architecture et roadmap |
| [`soutenance-order-api.pdf`](soutenance-order-api.pdf) | Support de présentation finale du projet |

---

## Architecture Decision Records (ADR)

Les ADR documentent les décisions techniques structurantes du projet.

| Fichier | Décision |
|---|---|
| [`adr/ADR-001-postgresql-comme-base-de-donnees.md`](adr/ADR-001-postgresql-comme-base-de-donnees.md) | Choix de PostgreSQL comme base de données |
| [`adr/ADR-002-architecture-en-couches.md`](adr/ADR-002-architecture-en-couches.md) | Choix d'une architecture en couches (Endpoint → Service → Repository) |
| [`adr/ADR-003-uuid-comme-cles-primaires.md`](adr/ADR-003-uuid-comme-cles-primaires.md) | Choix des UUID comme clés primaires |
| [`adr/ADR-004-redis-cache-multi-usages.md`](adr/ADR-004-redis-cache-multi-usages.md) | Choix de Redis comme cache multi-usages |
| [`adr/ADR-005-migration-asynchrone.md`](adr/ADR-005-migration-asynchrone.md) | Migration de l'architecture synchrone vers asynchrone |
| [`adr/ADR-006-docker-pour-la-conteneurisation.md`](adr/ADR-006-docker-pour-la-conteneurisation.md) | Choix de Docker pour la conteneurisation |
| [`adr/ADR-007-openpyxl-pour-les-exports.md`](adr/ADR-007-openpyxl-pour-les-exports.md) | *(Proposé)* openpyxl + csv pour les exports de données |
| [`adr/ADR-008-apscheduler-automatisation-kpi.md`](adr/ADR-008-apscheduler-automatisation-kpi.md) | *(Proposé)* APScheduler pour l'automatisation des rapports KPI |
| [`adr/ADR-009-pipeline-etl-oltp-olap.md`](adr/ADR-009-pipeline-etl-oltp-olap.md) | *(Proposé)* Pipeline ETL léger et séparation OLTP/OLAP |

---

## Fichiers à la racine du projet

| Fichier | Description |
|---|---|
| [`../README.md`](../README.md) | Présentation générale du projet |
| [`../CHANGELOG.md`](../CHANGELOG.md) | Historique des sprints (v0.1 → Sprint 4) |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | Guide d'installation et conventions de contribution |
| [`../DEVLOG.md`](../DEVLOG.md) | Journal technique détaillé (décisions, problèmes rencontrés, leçons apprises) |
