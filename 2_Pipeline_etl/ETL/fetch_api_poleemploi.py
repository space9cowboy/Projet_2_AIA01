import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import re

# Déterminer le chemin absolu vers le dossier data/raw à la racine
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# Charger les variables d'environnement
load_dotenv()
POLEEMPLOI_CLIENT_ID = os.getenv("POLEEMPLOI_CLIENT_ID")
POLEEMPLOI_CLIENT_SECRET = os.getenv("POLEEMPLOI_CLIENT_SECRET")

# Authentification pour obtenir le token OAuth2
auth_response = requests.post(
    "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire",
    data={
        "grant_type": "client_credentials",
        "client_id": POLEEMPLOI_CLIENT_ID,
        "client_secret": POLEEMPLOI_CLIENT_SECRET,
        "scope": "api_offresdemploiv2 o2dsoffre"
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

auth_response.raise_for_status()
auth_data = auth_response.json()
access_token = auth_data.get("access_token")

if not access_token:
    raise Exception("Impossible de récupérer le token d'accès.")

print("Token récupéré avec succès")

# Paramètres communs de la requête
BASE_URL = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
headers = {
    "Authorization": f"Bearer {access_token}"
}

all_jobs = []
start = 0
page_size = 150

while True:
    end = start + page_size - 1
    params = {
        "motsCles": "data scientist",
        "range": f"{start}-{end}",
        "insee": "75056"  # Paris
    }

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code in [200, 206]:
        data = response.json()
        offres = data.get("resultats", [])
        all_jobs.extend(offres)
        print(f"Offres récupérées : {len(offres)} pour le range {start}-{end}")

        if len(offres) < page_size:
            print("Fin de pagination atteinte.")
            break
        start += page_size
    else:
        print(f"Erreur pour le range {start}-{end} : {response.status_code}")
        break

# Traitement des données
jobs_api_poleemploi = []

for job in all_jobs:
    try:
        # Extraction directe
        salary_info = job.get("salaire", {})
        salary_min = salary_info.get("basSalaire")
        salary_max = salary_info.get("hautSalaire")
        description = job.get("description", "")

        # Si non précisé dans les champs, essayer de l'extraire depuis la description
        if not salary_min or not salary_max:
            matches = re.findall(r"(\d[\d\s]{2,}) ?€", description)
            cleaned_vals = [int(val.replace(" ", "")) for val in matches if val.replace(" ", "").isdigit()]

            if len(cleaned_vals) == 1:
                salary_min = salary_max = cleaned_vals[0]
            elif len(cleaned_vals) >= 2:
                salary_min = min(cleaned_vals)
                salary_max = max(cleaned_vals)

        jobs_api_poleemploi.append({
            "title": job.get("intitule"),
            "company": job.get("entreprise", {}).get("nom"),
            "location": job.get("lieuTravail", {}).get("libelle"),
            "created": job.get("dateCreation"),
            "category": job.get("romeCode"),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "contract_type": job.get("typeContratLibelle"),
            "description": description,
            "source": "API Pôle Emploi"
        })

    except Exception as e:
        print("Erreur de parsing :", e)
        continue


# Enregistrement CSV
output_path = os.path.join(RAW_DATA_PATH, "poleemploi_jobs.csv")
# os.makedirs(os.path.dirname(output_path), exist_ok=True)
df = pd.DataFrame(jobs_api_poleemploi)
df.to_csv(output_path, index=False)
print(f"{len(df)} Offres Pôle Emploi sauvegardées dans {output_path}")
