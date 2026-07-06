# Glossaire

Ce document définit les termes métier et techniques utilisés dans le projet Order API.

---

## Termes techniques

**Alembic**
Outil de versioning des migrations de schéma pour SQLAlchemy. Permet d'appliquer (`upgrade`) ou d'annuler (`downgrade`) des changements de schéma de façon déterministe.

**API REST headless**
Une API est un point d'accès standardisé qui permet à des systèmes de communiquer entre eux. REST désigne un style d'architecture basé sur des adresses web claires (ex. `GET /orders` pour lister les commandes). Headless signifie que le système ne fournit pas d'interface visuelle intégrée : il expose uniquement des données et des actions, que n'importe quelle interface (site web, application mobile, outil tiers) peut consommer librement.

**Backoffice**
Interface ou système de gestion interne d'une entreprise, invisible pour les clients finaux. C'est l'outil utilisé par les équipes pour gérer les commandes, les produits, les utilisateurs et les données, par opposition au front-end (la boutique visible par le client).

**AsyncSession**
Session SQLAlchemy asynchrone. Remplace la `Session` synchrone pour être compatible avec le fonctionnement asynchrone de FastAPI (voir ADR-005).

**CI/CD (Continuous Integration / Continuous Delivery)**
Pratique d'automatisation des tests et de la validation du code à chaque modification. Dans ce projet, gérée par GitHub Actions.

**FK (Foreign Key / Clé étrangère)**
Contrainte référentielle entre deux tables. Dans ce projet, les contraintes FK sont nommées explicitement pour permettre un rollback (`downgrade`) déterministe des migrations.

**Idempotence / Paiement idempotent**
Un paiement est dit idempotent lorsqu'il peut être soumis plusieurs fois sans produire d'effet supplémentaire : si un client clique deux fois sur "Payer" ou si le réseau renvoie la requête en double, la commande n'est débitée qu'une seule fois. Ce comportement est garanti par une clé unique (`Idempotency-Key`) transmise avec chaque requête de paiement et mémorisée dans Redis.

**JWT (JSON Web Token)**
Standard de token utilisé pour l'authentification. Le projet utilise un access token et un refresh token avec rotation, ainsi qu'une blacklist Redis pour les tokens révoqués.

**Lazy loading**
Mécanisme SQLAlchemy de chargement différé des relations. Le lazy loading par défaut est incompatible avec l'exécution asynchrone ; les relations doivent déclarer `lazy='selectin'` ou `lazy='joined'`.

**RBAC (Role-Based Access Control)**
Système de contrôle d'accès basé sur les rôles. Le backlog prévoit à terme quatre rôles métier (admin, manager, commercial, opérationnel), chacun déterminant précisément ce que l'utilisateur peut voir et faire - ex. un commercial pourrait consulter les commandes mais pas modifier le catalogue. Implémenté via une factory `require_role()` générique ; seuls `user` et `admin` sont réellement câblés dans le code à ce jour (`manager`/`operator`/`viewer` sont au stade Roadmap). Voir [Personas](../product/personas.md) pour le détail des rôles et leur état d'implémentation, vérifié via l'historique Git.

**Redis**
Base de données en mémoire utilisée dans ce projet comme cache multi-usages : idempotence des paiements, blacklist des tokens JWT révoqués, et rate limiting.

**Rate limiting**
Limitation du nombre de requêtes autorisées par IP ou par groupe de routes sur une période donnée, pour prévenir les abus.

**Repository (pattern)**
Couche d'abstraction qui isole les requêtes SQL de la logique métier. Voir ADR-002.

**UUID (Universally Unique Identifier)**
Identifiant unique généré côté application (et non par la base de données) utilisé comme clé primaire de toutes les tables. Voir ADR-003.

**Audit log**
Fichier (`audit_log.csv`) écrit par un middleware dédié, tracant les actions effectuées sur l'API. Il ne s'agit pas d'une table en base de données mais d'un artefact fichier.

**APScheduler** *(Roadmap)*
Bibliothèque Python de planification de tâches, prévue pour exécuter automatiquement le script de calcul des KPI quotidiens (voir [Data Dictionary](../product/data_dictionary.md)).

**ETL / Pipeline de données** *(Roadmap)*
Extract-Transform-Load. Chaîne de collecte, transformation et agrégation des données métier prévue pour alimenter les futurs KPI et dashboards métier.

**OLTP / OLAP** *(Roadmap)*
OLTP (On-Line Transactional Processing) désigne la base transactionnelle actuelle du projet. OLAP (On-Line Analytical Processing) désigne une séparation future envisagée pour isoler les requêtes analytiques/reporting de la base transactionnelle, afin d'optimiser les performances des dashboards.

---

## Termes métier

**Client (Customer)**
Acheteur externe de la plateforme, distinct d'un `User` (membre du staff). Une commande référence toujours un `Customer` via une clé étrangère.

**Commande (Order)**
Entité centrale du projet. Cycle de vie : brouillon → articles → paiement → livraison. Un utilisateur ne peut voir que ses propres commandes ; les mises à jour de statut sont réservées aux administrateurs.

**Facture (Invoice)**
Document généré automatiquement à chaque paiement réussi. Trace la personne l'ayant créée (`created_by`) et validée (`validated_by`, `validated_at`).

**Stock disponible**
Différence entre `stock_quantity` (quantité physiquement disponible) et `reserved_quantity` (quantité bloquée par des commandes non payées en cours). Le `stock_quantity` n'est décrémenté qu'à la confirmation du paiement.

**Utilisateur (User)**
Membre de l'équipe e-commerce (staff), par opposition à un `Customer`. Possède un rôle (actuellement `user` ou `admin`, voir [Personas](../product/personas.md)) qui détermine ses permissions.
