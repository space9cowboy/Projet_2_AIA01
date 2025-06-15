# Documentation du dashboard interactif

Ce document décrit le fonctionnement du **dashboard Streamlit** conçu pour visualiser les données analysées des offres d'emploi collectées et transformées.

---

## Objectifs du dashboard
- Offrir une interface interactive pour explorer les offres
- Visualiser les tendances par ville, source, métier, etc.
- Permettre le filtrage dynamique selon le titre ou la localisation

---

## Technologies utilisées
- **Streamlit** : interface web interactive en Python
- **Plotly**  : graphiques dynamiques (bar, pie, line...)
- **Seaborn & Matplotlib**  : visualisation avancée (boxplot, heatmap...)
- **Pandas**  : traitement et nettoyage des données
- **SQLAlchemy + psycopg2**  : connexion à PostgreSQL RDS (AWS)
- **Dotenv**  : gestion sécurisée des variables d'environnement

---

## Fichier principal
```bash
4_Dashboard/dashboard/dashboard.py
```

---

## Fonctionnalités principales
- **Chargement des données** depuis la base PostgreSQL RDS ou localement (`jobs_combined.csv`)
- **Filtrage** par mot-clé, ville, source
- **Graphiques interactifs** :
  - Top villes les plus dynamiques (bar chart)
  - Répartition des sources (pie chart)
  - Mots-clés fréquents dans les titres (word cloud)
  
---

## Lancement local du dashboard
```bash
streamlit run dashboard/dashboard.py
```

---

## Variables sensibles
Configurer un fichier `.env` à la racine avec :
```dotenv
DB_HOST=...
DB_PORT=5432
DB_NAME=...
DB_USER=...
DB_PASSWORD=...
```

---

## Améliorations possibles
- Authentification utilisateur avec Streamlit Authenticator
- Ajout de cartes (avec Folium ou Bokeh)
- Requêtes dynamiques directement depuis la base RDS
- Export CSV ou Excel via l’interface

---

> ℹ️ Le dashboard permet de mettre en valeur les données collectées tout au long du projet et constitue la vitrine visuelle de l’analyse.
