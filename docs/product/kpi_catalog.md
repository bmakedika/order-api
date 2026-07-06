# KPI Catalog

> ⚠️ **Note** : Order API distingue deux familles d'indicateurs : l'**observabilité technique** (Prometheus/Grafana, déjà implémentée) et les **KPI métier** (dashboards commandes/CA, exports, rapports automatisés - au stade backlog, EPICs 2 à 4). Les IDs `US*` renvoient aux user stories du [backlog v0.3.0](../order-api-project-documentation.pdf).

## Observabilité technique (implémentée)

### KPI-001

Nom : Requêtes HTTP totales

Calcul : `http_requests_total`

Source : endpoint `/metrics` (Prometheus)

Statut : ✅ Implémenté

---

### KPI-002

Nom : Latence des requêtes (p95)

Calcul : `http_request_duration_seconds` (percentile 95)

Source : dashboard Grafana technique

Statut : ✅ Implémenté

---

### KPI-003

Nom : Débit (RPS - Requests Per Second)

Calcul : dérivé de `http_requests_total` dans le temps

Source : dashboard Grafana technique

Statut : ✅ Implémenté

---

### KPI-004

Nom : Taux d'erreur (technique)

Calcul : proportion de réponses en erreur sur `http_requests_total`

Source : dashboard Grafana technique

Statut : ✅ Implémenté

---

## KPI métier - EPIC 2 : Exports de données (Roadmap)

### KPI-005

Nom : Export des commandes (CSV)

User story : US5

Statut : 🔜 Roadmap

---

### KPI-006

Nom : Export des produits (CSV)

User story : US6

Statut : 🔜 Roadmap

---

### KPI-007

Nom : Export des utilisateurs (CSV)

User story : US7

Statut : 🔜 Roadmap

---

### KPI-008

Nom : Export des factures (Excel .xlsx)

User story : US8

Statut : 🔜 Roadmap

---

## KPI métier - EPIC 3 : Tableaux de bord métier Grafana (Roadmap)

### KPI-009

Nom : Commandes par jour

Calcul : `COUNT(orders)` groupé par jour

User story : US10

Statut : 🔜 Roadmap

---

### KPI-010

Nom : Temps de traitement moyen des commandes

User story : US11

Statut : 🔜 Roadmap

---

### KPI-011

Nom : Alerte taux d'erreur métier (> 5%)

User story : US12

Statut : 🔜 Roadmap

---

### KPI-012

Nom : Chiffre d'affaires par jour

User story : US13

Statut : 🔜 Roadmap

---

## KPI métier - EPIC 4 : Pipeline de données & automatisation (Roadmap)

### KPI-013

Nom : Script KPI quotidien (`scripts/kpi_report.py`)

Calcul : nombre de commandes, délai moyen de paiement, taux d'erreur - exécution automatique via APScheduler à 06h00

User story : US14, US15, US16

Statut : 🔜 Roadmap

---

### KPI-014

Nom : Historique des KPI (table analytique dédiée)

User story : US17

Statut : 🔜 Roadmap
