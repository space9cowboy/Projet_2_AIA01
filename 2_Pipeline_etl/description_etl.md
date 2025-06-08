# 🔌 Description du pipeline ETL

Ce document fournit une vue d'ensemble du pipeline **ETL (Extract, Transform, Load)** mis en place dans le cadre du projet "Infrastructure Data sur le Cloud".

---

## Objectif du pipeline
Permettre la collecte, le nettoyage, la standardisation et le chargement de données d’offres d’emploi dans une base PostgreSQL RDS afin de faciliter l'analyse et la visualisation.

---

## ETAPE 1 : EXTRACT – Collecte de données

### Sources utilisées
- **AI Jobs** (scraping HTML avec `requests` + `BeautifulSoup`)
- **Adzuna API** (requêtes `GET` via `requests`)

### Format de sortie
- Fichiers CSV dans `data/raw/`
  - `aijobs_jobs.csv`
  - `adzuna_jobs.csv`

### Script concernés
```bash
etl/
├── scrape_aijobs.py
└── fetch_api_adzuna.py
```

---

## ETAPE 2 : TRANSFORM – Nettoyage et standardisation

### Traitements appliqués
- Normalisation des noms de colonnes : `title`, `company`, `location`, `source`
- Suppression des valeurs manquantes
- Fusion des datasets avec `pandas.concat`

### Objectif
Avoir un fichier unique et propre : `jobs_combined.csv`
Ce fichier va regrouper l'ensemble des offres que l'on a extrait depuis Ai Jobs et Adzuna.

### Script concerné
```bash
etl/transform_jobs.py
```

### Format de sortie
- `data/cleaned/jobs_combined.csv`

---

## ETAPE 3 : LOAD – Chargement en base PostgreSQL RDS

### Outils
- `sqlalchemy` + `psycopg2`
- Connexion à une instance RDS PostgreSQL

### Contenu chargé
- Fichier `jobs_combined.csv` inséré dans une table `job_offers`

### Script utilisé
```bash
etl/load_to_rds.py
```

---

## Automatisation
L'ensemble du pipeline peut être réexécuté en local ou en cloud avec les scripts Python.


---

## Avantages du pipeline
- Facilement maintenable et réutilisable
- Compatible cloud (S3, RDS)
- Données standardisées, prêtes pour l'analyse

> Tous les scripts ETL sont présents dans le dossier `etl/` et documentés en commentaires.
