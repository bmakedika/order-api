# Guide de contribution

Ce document décrit comment installer le projet en local, les conventions de code et les règles de contribution.

---

## Prérequis

- Python 3.11+
- Docker Desktop
- Git

---

## Installation en local

### 1. Cloner le projet

```bash
git clone https://github.com/bmakedika/order-api.git
cd order-api-python
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env avec vos propres valeurs
```

> **Astuce :** utiliser un mot de passe sans caractères spéciaux pour `POSTGRES_PASSWORD` et `DATABASE_URL` afin d'éviter les problèmes d'encodage d'URL.

### 5. Démarrer l'infrastructure

```bash
docker compose up -d
```

### 6. Appliquer les migrations

```bash
alembic upgrade head
```

> Si les migrations échouent (volume Docker avec d'anciens identifiants) :
>
> ```bash
> docker compose down -v
> docker compose up -d
> alembic upgrade head
> ```
>
> ⚠️ Cette commande supprime toutes les données existantes.

### 7. Lancer l'API

```bash
uvicorn app.main:app --reload --env-file .env
```

L'API est disponible sur `http://localhost:8000/docs`

---

## Monitoring (optionnel)

```bash
docker compose -f docker-compose.monitoring.yml up -d
```

| Service     | URL                             | Identifiants  |
| ----------- | -------------------------------- | ------------- |
| Grafana     | `http://localhost:3001`          | admin / admin |
| Prometheus  | `http://localhost:9090`          | -             |
| Métriques API | `http://localhost:8000/metrics` | -             |

Le dashboard **Order API - Overview** est auto-chargé dans Grafana (provisioning).

---

## Tests

```bash
# Lancer tous les tests
pytest -v

# Avec couverture
pytest --cov=app --cov-report=term-missing
```

La suite de tests utilise une base SQLite en mémoire et un Redis isolé (flushdb avant chaque test). Aucune dépendance à l'infrastructure Docker.

---

## Commandes utiles

```bash
# Redémarrer l'infrastructure
docker compose down && docker compose up -d

# Créer une nouvelle migration
alembic revision --autogenerate -m "description"

# Appliquer les migrations
alembic upgrade head

# Annuler une migration
alembic downgrade -1

# Lancer les tests en mode verbeux
pytest -v

# Vérifier le linting
ruff check app/
```

---

## Conventions de code

- **Python** : PEP 8
- **Architecture** : respecter la séparation en couches `Endpoint → Service → Repository` (voir [ADR-002](docs/adr/ADR-002-architecture-en-couches.md))
- **Clés primaires** : UUID générés côté application, jamais d'entiers auto-incrémentés (voir [ADR-003](docs/adr/ADR-003-uuid-comme-cles-primaires.md))
- **Relations SQLAlchemy** : toujours déclarer `lazy='selectin'` ou `lazy='joined'` (obligatoire en async, voir [ADR-005](docs/adr/ADR-005-migration-asynchrone.md))
- **Migrations** : toute contrainte de clé étrangère doit être nommée explicitement pour un `downgrade()` déterministe
- **Variables d'environnement** : toujours via `.env`, jamais en dur dans le code

---

## Conventions de commit

Ce projet suit le standard [Conventional Commits](https://www.conventionalcommits.org/), avec des commits atomiques (une action par commit).

Format :

```
type(scope): description courte
```

| Type       | Usage                                                |
| ---------- | ----------------------------------------------------- |
| `feat`     | Nouvelle fonctionnalité                               |
| `fix`      | Correction de bug                                     |
| `docs`     | Modification de documentation                         |
| `refactor` | Refactoring sans changement de comportement           |
| `test`     | Ajout ou modification de tests                        |
| `chore`    | Tâches techniques (dépendances, config, gitignore)    |

Exemples (tirés de l'historique du projet) :

```bash
refactor(db): migrate synchronous session to AsyncSession
fix(sqlalchemy): add lazy='selectin' to relationships to fix MissingGreenlet
test(orders): migrate test suite to AsyncClient and aiosqlite
refactor(orders): replace free-form customer_id with UUID FK to customers
chore(requirements): add greenlet dependency for Python 3.14
```

---

## Structure du projet

```
order-api/
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── middlewares/
├── alembic/                    # migrations de schéma
├── tests/                      # suite de tests async (pytest-asyncio)
├── docs/                       # documentation projet
│   ├── adr/                    # Architecture Decision Records
│   ├── gouvernance/
│   └── product/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docker-compose.yml
├── docker-compose.monitoring.yml
├── requirements.txt
├── DEVLOG.md
└── README.md
```
