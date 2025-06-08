# ⛅️ Documentation de l'infrastructure Cloud (AWS)

Ce document décrit les composants cloud mis en place dans le cadre du projet, ainsi que les étapes de création de l'infrastructure sur AWS (S3 et RDS).

---

## 1. Data Lake – Bucket S3

### Objectif
Stocker les données brutes collectées (scraping et API) ainsi que les données nettoyées, de façon scalable et sécurisée.

### Création du bucket
1. Se connecter à la [console AWS S3](https://s3.console.aws.amazon.com/s3)
2. Cliquer sur **"Create bucket"**
3. Donner un nom unique (ex: `projet-data-cloud`)
4. Choisir la région (ex: `eu-west-3` - Paris)
5. Désactiver le blocage de l'accès public (si besoin)
6. Laisser les autres options par défaut
7. Créer le bucket

### Structure adopté
```
data/
├── raw/                            # Données brutes
        aijobs_jobs.csv
        api_jobs_adzuna.csv             
└── cleaned/                        # Données nettoyées prêtes à charger
        jobs_combined.csv              
```

---

## 2. Data Warehouse – PostgreSQL RDS

### Objectif
Stocker les données nettoyées dans une base relationnelle afin de permettre des requêtes SQL, l'analyse et l'alimentation du dashboard.

### Création de l'instance RDS
1. Se rendre sur [console AWS RDS](https://console.aws.amazon.com/rds/)
2. Cliquer sur **"Create database"**
3. Choisir **PostgreSQL** comme moteur
4. Sélectionner :
   - Mode de création : Standard
   - Engine version : PostgreSQL 15+ 
   - Nom de l’instance : `projet-data-cloud`
   - Nom d’utilisateur : ex. `admin`
   - Mot de passe : ex. `Sljndfljkbmfk7hk9@`
5. Activer le mode de déploiement public ("Public access" sur YES)
6. Laisser les autres options par défaut et créer la base

### Connexion
- Hôte : `votre-endpoint-rds.amazonaws.com`
- Port : `5432`
- Base : `projet-data-cloud`
- Utilisateur : `admin`
- Mot de passe : `Sljndfljkbmfk7hk9@`

### Test de connexion
Via PgAdmin ou via Python avec `psycopg2` / `sqlalchemy`

---

## 📊 Diagramme Architecture (Vue d'ensemble)

```
[Scraping/API]
     ⬇️
 [data/raw/*.csv] ➔ [S3 Bucket]
     ⬇️
[Transformation]
     ⬇️
 [data/cleaned/*.csv]
     ⬇️          ⬇️
 [S3 Bucket]       [PostgreSQL RDS]
                             ⬇️
                        [Dashboard Streamlit]
```

---

## Avantages de cette infrastructure
- Stockage scalable et accessible
- Intégration native avec d’autres services AWS
- Possibilité de créer des dashboards alimentés en direct
- Structure proche de ce que l’on retrouve en entreprise

---

> ℹ️ Ne pas oublier pas de gérer les accès via IAM et de conserver vos clés AWS secrètes dans un `.env` ou via le gestionnaire de secrets AWS.
