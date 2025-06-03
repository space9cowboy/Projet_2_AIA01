import os
import pandas as pd

# Déterminer les chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
RAW_DATA_PATH = os.path.join(ROOT_DIR, "data", "raw")
CLEANED_DATA_PATH = os.path.join(ROOT_DIR, "data", "cleaned")
os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

# Charger les fichiers CSV
aijobs_path = os.path.join(RAW_DATA_PATH, "aijobs_jobs.csv")
adzuna_path = os.path.join(RAW_DATA_PATH, "api_jobs_adzuna.csv")

aijobs_df = pd.read_csv(aijobs_path)
adzuna_df = pd.read_csv(adzuna_path)

# Nettoyage AI-jobs
aijobs_df = aijobs_df.rename(columns={
    "title": "title",
    "company": "company",
    "location": "location"
})
aijobs_df["salary_min"] = None
aijobs_df["salary_max"] = None
aijobs_df["contract_type"] = None

# Normaliser les valeurs
aijobs_df["title"] = aijobs_df["title"].astype(str).str.strip().str.lower()
aijobs_df["company"] = aijobs_df["company"].astype(str).str.strip()
aijobs_df["location"] = aijobs_df["location"].astype(str).str.strip()
aijobs_df["source"] = "AI-jobs.net"

# Nettoyage Adzuna
adzuna_df = adzuna_df.rename(columns={
    "title": "title",
    "company": "company",
    "location": "location",
    "salary_min": "salary_min",
    "salary_max": "salary_max",
    "contract_type": "contract_type",
    "source": "source"
})
adzuna_df["title"] = adzuna_df["title"].astype(str).str.strip().str.lower()
adzuna_df["company"] = adzuna_df["company"].astype(str).str.strip()
adzuna_df["location"] = adzuna_df["location"].astype(str).str.strip()
adzuna_df["source"] = "Adzuna API"

# Harmoniser les colonnes
common_cols = ["title", "company", "location", "salary_min", "salary_max", "contract_type", "source"]
aijobs_df = aijobs_df[common_cols]
adzuna_df = adzuna_df[common_cols]

# Fusionner les deux jeux de données
combined_df = pd.concat([aijobs_df, adzuna_df], ignore_index=True)

# Supprimer les doublons
combined_df.drop_duplicates(inplace=True)

# Enregistrer le fichier nettoyé
output_path = os.path.join(CLEANED_DATA_PATH, "jobs_combined.csv")
combined_df.to_csv(output_path, index=False)
print(f"Données nettoyées et fusionnées enregistrées dans : {output_path}")
print(f"Nombre total d'offres : {len(combined_df)}")
