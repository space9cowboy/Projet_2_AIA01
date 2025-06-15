# 🔌 Description du pipeline ETL

Ce document fournit une vue d'ensemble du pipeline **ETL (Extract, Transform, Load)** mis en place dans le cadre du projet "Infrastructure Data sur le Cloud".

---

## Objectif du pipeline
Permettre la collecte, le nettoyage, la standardisation et le chargement de données d’offres d’emploi dans une base PostgreSQL RDS afin de faciliter l'analyse et la visualisation interactive via un dashboard Streamlit.

---

## ETAPE 1 : EXTRACT – Collecte de données

### Sources utilisées
- **AI Jobs** (scraping HTML avec `requests` + `BeautifulSoup`)
- **Adzuna API** (requêtes `GET` via `requests`)
- **API Pôle Emploi** (via `requests` avec authentification OAuth2)

### Format de sortie
- Fichiers CSV dans `data/raw/`
  - `aijobs_jobs.csv`
  - `adzuna_jobs.csv`
  - `poleemploi_jobs.csv`

### Scripts concernés
```bash
etl/
├── scrape_aijobs.py
├── fetch_api_adzuna.py
└── fetch_api_poleemploi.py
```

---

## ETAPE 2 : TRANSFORM – Nettoyage et standardisation

### Traitements appliqués
- Normalisation des noms et des valeurs (source, entreprise, ville)
- Suppression des doublons et valeurs manquantes critiques
- Standardisation des champs `salary_min`, `salary_max`, `contract_type`
- Enrichissement éventuel via géocodage ou mapping
- Fusion des datasets via `pandas.concat`

### Objectif
Avoir un fichier unique et propre : `jobs_combined.csv` regroupant toutes les offres standardisées

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
- Connexion à une instance RDS PostgreSQL sur AWS

### Contenu chargé
- Table `jobs` dans la base, avec les colonnes :
  - `title`, `company`, `location`, `salary_min`, `salary_max`, `contract_type`, `source`, `publication_date`, etc.

### Script utilisé
```bash
etl/load_to_rds.py
```

---


## Visualisation interactive

- Dashboard développé avec **Streamlit**
- Visualisations dynamiques avec **Plotly**, **Seaborn**, **Matplotlib**
- Filtrage interactif (localisation, source, entreprise, salaire...)
- Calculs et KPIs intégrés : insights sur les salaires, les offres, les postes, etc.

---

## Avantages du pipeline
- Modulaire, évolutif, et maintenable facilement
- Compatible Cloud (RDS, S3)
- Données nettoyées, enrichies et prêtes pour la BI
- Permet l'exploration immédiate via le dashboard

> Tous les scripts ETL sont présents dans le dossier `etl/` et commentés pour la réutilisation.
