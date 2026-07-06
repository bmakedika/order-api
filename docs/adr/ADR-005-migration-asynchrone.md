# ADR-005 - Migration vers une architecture asynchrone

## Statut

Accepté

## Date

À compléter (Sprint 3)

## Contexte

FastAPI est un framework asynchrone. L'utilisation d'une session SQLAlchemy synchrone (`Session`) dans un contexte async bloque le thread principal à chaque requête SQL, annulant les bénéfices de performance de FastAPI.

## Décision

Migrer l'ensemble de la stack - base de données, services, endpoints et tests - vers un fonctionnement **asynchrone** (`AsyncSession`, `create_async_engine`, `async def`/`await`).

## Justification

- Conserve les bénéfices de performance natifs de FastAPI
- Cohérence de bout en bout entre le framework web et la couche d'accès aux données

## Conséquences

- Toutes les relations SQLAlchemy doivent déclarer `lazy='selectin'` ou `lazy='joined'` - le lazy loading par défaut est incompatible avec l'async et provoque une erreur `MissingGreenlet`
- `greenlet` doit être ajouté explicitement à `requirements.txt` (n'est plus fourni par défaut à partir de Python 3.14)
- La suite de tests a dû être migrée vers `AsyncClient`/`aiosqlite`/`pytest-asyncio`, avec `StaticPool` obligatoire pour SQLite en mémoire (sans quoi chaque connexion recrée une base vide)
- La configuration `DATABASE_URL` doit être adaptée pour ajouter le préfixe async approprié (`sqlite+aiosqlite://` ou `postgresql+psycopg://`), y compris en CI GitHub Actions
