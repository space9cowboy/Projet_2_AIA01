import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# 💡 Déterminer le chemin absolu vers le dossier data/raw depuis n'importe où
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # racine du projet
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# URL de l'API Adzuna France
url = "https://api.adzuna.com/v1/api/jobs/fr/search/1"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 50,
    "what": "data science",  # mots-clés
    "content-type": "application/json"
}

# Requête API
response = requests.get(url, params=params)
data = response.json()

jobs = []

for result in data.get("results", []):
    jobs.append({
        "title": result.get("title"),
        "company": result.get("company", {}).get("display_name"),
        "location": result.get("location", {}).get("display_name"),
        "created": result.get("created"),
        "category": result.get("category", {}).get("label"),
        "salary_min": result.get("salary_min"),
        "salary_max": result.get("salary_max"),
        "contract_type": result.get("contract_type"),
        "description": result.get("description"),
        "source": "Adzuna API"
    })

# Enregistrement du fichier CSV dans le bon dossier
output_file = os.path.join(RAW_DATA_PATH, "api_jobs_adzuna.csv")
df = pd.DataFrame(jobs)
df.to_csv(output_file, index=False)
print(f"✅ {len(df)} offres API Adzuna enregistrées dans {output_file}")
