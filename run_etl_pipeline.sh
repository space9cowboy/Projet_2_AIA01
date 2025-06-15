#!/bin/bash

# ======================================
# Script d'exécution du pipeline ETL complet
# Projet : Infrastructure Data sur le Cloud
# ======================================

echo -e "\nDémarrage du pipeline ETL complet..."

# Aller dans le dossier des scripts ETL selon la structure actuelle
cd 2_Pipeline_etl/ETL || { echo "Dossier ETL introuvable. Vérifie la structure du projet."; exit 1; }

# Étape 1 : Extraction
echo -e "\nÉtape 1.1 : Scraping depuis AI Jobs..."
python scrape_aijobs.py || { echo "Erreur lors du scraping AI Jobs"; exit 1; }

echo -e "\nÉtape 1.2 : Récupération via l'API Adzuna..."
python fetch_api_adzuna.py || { echo "Erreur lors de l'appel API Adzuna"; exit 1; }

echo -e "\n Étape 1.3 : Récupération via l'API Pôle Emploi..."
python fetch_api_poleemploi.py || { echo "Erreur lors de l'appel API Pôle Emploi"; exit 1; }

# Étape 2 : Transformation
echo -e "\nÉtape 2 : Nettoyage, fusion et normalisation..."
python transform_jobs.py || { echo "Erreur lors de la transformation des données"; exit 1; }

# Étape 3 : Chargement
echo -e "\nÉtape 3 : Insertion dans la base PostgreSQL RDS..."
python load_to_rds.py || { echo "Erreur lors du chargement dans la base PostgreSQL"; exit 1; }

# Retour à la racine du projet
cd ../../..

echo -e "\nPipeline ETL exécuté avec succès. Les données sont prêtes pour l'analyse via le dashboard Streamlit."