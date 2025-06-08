import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Déterminer le chemin absolu vers le dossier data/raw à la racine
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# URL avec filtre Data Science
BASE_URL = "https://aijobs.net/?cat=3&cou=78&reg=3&key=&exp=&sal="
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(BASE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Conteneur général des offres : chaque ligne de job dans "div.row"
offers = soup.find_all("div", class_="row")

jobs_aijobs = []

for offer in offers:
    try:
        title_elem = offer.find("h5", class_="fw-normal text-body-emphasis text-break")
        if not title_elem:
            continue  # pas une offre
        title = title_elem.text.strip()

        company_elem = offer.find("span", class_="text-muted")
        company = company_elem.text.strip() if company_elem else "N/A"

        location_elem = offer.find("span", class_="d-none d-md-block text-break mb-1")
        location = location_elem.text.strip() if location_elem else "N/A"
        
        salary_elem = offer.find("div", class_="d-block mb-4")
        salary = salary_elem.text.strip() if salary_elem else "N/A"
        
        contract_type_elem = offer.find("span", class_="badge rounded-pill text-bg-secondary my-md-1 ms-1")
        contract_type = contract_type_elem.text.strip() if contract_type_elem else "N/A"

        jobs_aijobs.append({
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "contract_type": contract_type,
            "source": "AI-jobs.net"
        })

    except Exception as e:
        print("Erreur lors de l'extraction d'une offre :", e)
        continue


# Export CSV dans data/raw à la racine
output_path = os.path.join(RAW_DATA_PATH, "aijobs_jobs.csv")
df = pd.DataFrame(jobs_aijobs)
df.to_csv(output_path, index=False)
print(f"{len(df)} Offres Aijobs enregistrées dans {output_path}")