import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Déterminer le chemin absolu vers le dossier data/raw à la racine
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# URL API
base_url = "https://api.adzuna.com/v1/api/jobs/fr/search/"
params_base = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 50,
    "what": "data science",
    "content-type": "application/json"
}

jobs = []
max_pages = 20
min_new_results = 5  # Si moins de 5 résultats sur une page = fin

for page in range(1, max_pages + 1):
    print(f"Recherche des différentes offres sur la Page {page}")
    url = base_url + str(page)
    response = requests.get(url, params=params_base)

    if response.status_code != 200:
        print(f"Erreur sur la page {page} : {response.status_code}")
        break

    data = response.json()
    results = data.get("results", [])
    
    print(f"{len(results)} Offres via Adzuna API récupérés")

    if len(results) < min_new_results:
        print("Fin détectée (peu de résultats)")
        break

    for result in results:
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

# Enregistrement CSV
output_file = os.path.join(RAW_DATA_PATH, "api_jobs_adzuna.csv")
df = pd.DataFrame(jobs)
df.to_csv(output_file, index=False)
print(f"{len(df)} offres API Adzuna enregistrées dans {output_file}")
