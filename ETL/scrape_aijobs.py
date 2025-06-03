import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# Crée le dossier de stockage s'il n'existe pas
os.makedirs("data/raw", exist_ok=True)

# URL avec filtre Data Science
url = "https://aijobs.net/?cat=3&key=&exp=&sal="

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Conteneur général des offres : chaque ligne de job dans "div.row"
offers = soup.find_all("div", class_="row")

jobs = []

for offer in offers:
    try:
        title_elem = offer.find("h5", class_="fw-normal text-body-emphasis text-break")
        if not title_elem:
            continue  # pas une offre
        title = title_elem.text.strip()

        company_elem = offer.find("span", class_="text-muted")
        company = company_elem.text.strip() if company_elem else "N/A"

        location_elem = offer.find("div", class_="text-end")
        location = location_elem.text.strip() if location_elem else "N/A"

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "source": "AI-jobs.net"
        })

    except Exception as e:
        print("Erreur lors de l'extraction d'une offre :", e)
        continue

# Export CSV
df = pd.DataFrame(jobs)
df.to_csv("data/raw/aijobs_jobs.csv", index=False)
print(f"{len(df)} offres extraites et enregistrées dans data/raw/aijobs_jobs.csv")
