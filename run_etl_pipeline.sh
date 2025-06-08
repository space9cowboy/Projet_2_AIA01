#!/bin/bash

# === Script d'exécution du pipeline ETL complet ===

echo "\n Démarrage du pipeline ETL complet"

cd 2_Pipeline_etl/ETL || { echo "Dossier ETL introuvable"; exit 1; }

# Étape 1 : Extraction
echo "\n Étape 1 : Scraping AI Jobs..."
python scrape_aijobs.py || exit 1

echo "\n Étape 1 : Appel API Adzuna..."
python fetch_api_adzuna.py || exit 1

# Étape 2 : Transformation
echo "\n Étape 2 : Nettoyage et transformation..."
python transform_jobs.py || exit 1

# Étape 3 : Chargement dans PostgreSQL RDS
echo "\n Étape 3 : Chargement dans la base PostgreSQL RDS..."
python load_to_rds.py || exit 1

cd ../../..

echo "\n Pipeline ETL exécuté avec succès. Les données sont prêtes pour l'analyse."
