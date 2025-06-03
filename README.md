# 🧠 Analyse des Offres d’Emploi dans les Métiers de la Data

Projet pédagogique complet visant à mettre en place une **infrastructure data sur le cloud** (AWS), depuis la **collecte de données** jusqu’à leur **analyse visuelle interactive** via un dashboard Streamlit.

---

## 📌 Objectifs

- Collecter des offres d’emploi dans la data via **scraping web** et **API**
- Nettoyer, fusionner et transformer les données en un dataset unifié
- Stocker les données dans le cloud avec **AWS S3** et **PostgreSQL RDS**
- Réaliser une **analyse statistique** et des visualisations pertinentes
- Proposer un **dashboard web interactif** avec Streamlit

---

## 🛠️ Technologies utilisées

| Domaine          | Outils / Services                                   |
|------------------|-----------------------------------------------------|
| Langage          | Python (3.10+)                                      |
| Web scraping     | BeautifulSoup, Requests, Selenium                   |
| API              | Adzuna API                                          |
| Stockage         | AWS S3                                              |
| Base de données  | PostgreSQL via AWS RDS                              |
| Traitement data  | Pandas                                              |
| Visualisation    | Plotly, Seaborn, Streamlit                          |
| Sécurité         | Dotenv (.env)                                       |

---

## 📁 Structure du projet

```
projet_data_cloud/
├── data/
│   ├── raw/           # Fichiers bruts (scraping, API)
│   └── cleaned/       # Dataset transformé
├── etl/               # Scripts de collecte et transformation
├── dashboard/
│   └── dashboard.py   # Dashboard Streamlit interactif
├── notebooks/         # Analyses locales
├── .env               # Variables d’environnement (non versionné)
├── requirements.txt   # Dépendances Python
└── README.md
```

---

## 🚀 Lancement du dashboard

### 1. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer vos variables `.env`
```
DB_HOST=...
DB_PORT=...
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
```

### 3. Lancer Streamlit
```bash
streamlit run dashboard/dashboard.py
```

---

## 📊 Résultats

- +200 offres analysées (data analyst, scientist, ML engineer…)
- Top villes : Paris, Lyon, Toulouse…
- Visualisations interactives (barplot, pie chart, boxplot)
- Données stockées durablement dans le cloud AWS

---

## 📈 Perspectives

- Déploiement du dashboard sur Streamlit Cloud
- Enrichissement via d’autres APIs (LinkedIn, Indeed)
- Automatisation via Airflow ou AWS Lambda

---

## 👨‍💼 Réalisé dans le cadre d’un projet école – 2025
