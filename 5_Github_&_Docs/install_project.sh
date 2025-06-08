#!/bin/bash

# === Script d'installation automatique du projet ===

echo "🚀 Initialisation de l'environnement virtuel..."
python3 -m venv venv
source venv/bin/activate

echo "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Dépendances installées avec succès."
echo ""
echo "N'oubliez pas de configurer votre fichier .env :"
echo "DB_HOST=..."
echo "DB_PORT=5432"
echo "DB_NAME=..."
echo "DB_USER=..."
echo "DB_PASSWORD=..."
echo ""
echo "Pour lancer le dashboard :"
echo "streamlit run dashboard/dashboard.py"