# Data Dictionary

Ce document décrit les entités du projet Order API telles que documentées dans le DEVLOG et le README.

> ⚠️ **Note sur la complétude** : contrairement au Data Dictionary de RetailFlow (généré à partir des fichiers de schéma DBT), les sources fournies pour Order API (`README.md`, `DEVLOG.md`) ne détaillent pas l'intégralité des colonnes de chaque table. Seules les colonnes explicitement mentionnées dans ces sources sont listées ci-dessous. **À compléter par Bienvenu à partir de `app/models/` pour une liste exhaustive des colonnes.**

---

## `users`

**Description** : Membre de l'équipe e-commerce (staff), par opposition à un client externe (`customers`).

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique généré côté application (clé primaire) |
| `role` | - | Rôle RBAC de l'utilisateur : `user` (v0.2.0) et `admin` (v0.3.0) réellement câblés dans le code. `manager`/`operator`/`viewer` sont au stade Roadmap (voir [Personas](personas.md)) |

*Colonnes additionnelles (mot de passe, email, etc.) non détaillées dans les sources fournies.*

---

## `customers`

**Description** : Acheteur externe de la plateforme, distinct des membres du staff (`users`). Table introduite en v0.3.0 avec ses propres modèle, schémas, service et endpoints CRUD. Reliée par clé étrangère UUID à `orders` **et** `invoices`.

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique généré côté application (clé primaire) |

*Colonnes additionnelles non détaillées dans les sources fournies.*

---

## `products`

**Description** : Catalogue produits. CRUD complet réservé aux administrateurs ; lecture publique (GET) sans authentification.

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique généré côté application (clé primaire) |
| `stock_quantity` | - | Quantité physiquement disponible en entrepôt |
| `reserved_quantity` | - | Quantité bloquée par des commandes non payées en cours |

**Calcul** :

```
stock disponible = stock_quantity - reserved_quantity
```

`stock_quantity` n'est décrémenté qu'à la confirmation du paiement. Si une commande est abandonnée, la quantité réservée est libérée sans impact sur le stock physique.

*Colonnes additionnelles (nom, prix, etc.) non détaillées dans les sources fournies.*

---

## `orders`

**Description** : Commande, entité centrale du projet. Cycle de vie : brouillon → articles → paiement → livraison.

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique généré côté application (clé primaire) |
| `customer_id` | UUID FK | Référence vers `customers.id`. Remplace l'ancienne colonne `String` libre sans intégrité référentielle (Sprint 2). Contrainte nommée `fk_orders_customer_id` |
| `user_id` | UUID FK, nullable | Référence vers `users.id`. Nullable car une commande peut être passée directement par un client sans intervention du staff |
| `status` | - | Statut du cycle de vie de la commande. Les mises à jour de statut sont réservées aux administrateurs |

*Colonnes additionnelles non détaillées dans les sources fournies.*

---

## `invoices`

**Description** : Facture générée automatiquement à chaque paiement réussi.

| Colonne | Type | Description |
|---|---|---|
| `id` | UUID | Identifiant unique généré côté application (clé primaire) |
| `created_by` | - | Traçabilité : auteur de la création de la facture |
| `validated_by` | - | Traçabilité : auteur de la validation de la facture |
| `validated_at` | - | Date/heure de validation de la facture |
| `id_payment` | - | Référence au paiement. **Pas de FK locale actuellement** - une intégration Stripe est à planifier (amélioration identifiée pour les sprints futurs) |

*Colonnes additionnelles non détaillées dans les sources fournies.*

---

## Relations entre les tables

```
users ─────────────► orders (user_id, nullable)
customers ─────────► orders (customer_id, FK obligatoire)
customers ─────────► invoices (FK UUID)
orders ─────────────► invoices (paiement réussi)
products ───────────► orders (via articles de commande - table de jointure non détaillée dans les sources)
```

## Artefacts hors base de données

**`audit_log.csv`**
Fichier généré par le middleware d'audit, tracant les actions effectuées sur l'API. Ce n'est pas une table en base de données.
