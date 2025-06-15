import os
import pandas as pd

# Déterminer les chemins
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))
RAW_DATA_PATH = os.path.join(ROOT_DIR, "data", "raw")
CLEANED_DATA_PATH = os.path.join(ROOT_DIR, "data", "cleaned")
os.makedirs(CLEANED_DATA_PATH, exist_ok=True)

# Charger les fichiers CSV
aijobs_df = pd.read_csv(os.path.join(RAW_DATA_PATH, "aijobs_jobs.csv"))
adzuna_df = pd.read_csv(os.path.join(RAW_DATA_PATH, "api_jobs_adzuna.csv"))
poleemploi_df = pd.read_csv(os.path.join(RAW_DATA_PATH, "poleemploi_jobs.csv"))

# Harmonisation AIJobs
aijobs_df = aijobs_df.rename(columns={
    "salary": "salary_raw"
})
aijobs_df["salary_min"] = None
aijobs_df["salary_max"] = None
aijobs_df["created"] = None
aijobs_df["category"] = None
aijobs_df["description"] = None

# Nettoyage et normalisation AIJobs
aijobs_df["title"] = aijobs_df["title"].astype(str).str.strip().str.lower()
aijobs_df["company"] = aijobs_df["company"].astype(str).str.strip()
aijobs_df["location"] = aijobs_df["location"].astype(str).str.strip()

# Harmonisation Adzuna
adzuna_df["title"] = adzuna_df["title"].astype(str).str.strip().str.lower()
adzuna_df["company"] = adzuna_df["company"].astype(str).str.strip()
adzuna_df["location"] = adzuna_df["location"].astype(str).str.strip()

# Harmonisation Pôle Emploi
poleemploi_df["title"] = poleemploi_df["title"].astype(str).str.strip().str.lower()
poleemploi_df["company"] = poleemploi_df["company"].astype(str).str.strip()
poleemploi_df["location"] = poleemploi_df["location"].astype(str).str.strip()

# Colonnes communes à conserver
common_cols = [
    "title", "company", "location", "salary_min", "salary_max",
    "contract_type", "description", "created", "category", "source"
]

# Ajouter les colonnes manquantes à AIJobs
for col in common_cols:
    if col not in aijobs_df.columns:
        aijobs_df[col] = None
aijobs_df = aijobs_df[common_cols]

# Ajouter les colonnes manquantes à Adzuna
for col in common_cols:
    if col not in adzuna_df.columns:
        adzuna_df[col] = None
adzuna_df = adzuna_df[common_cols]

# Ajouter les colonnes manquantes à Pôle Emploi
for col in common_cols:
    if col not in poleemploi_df.columns:
        poleemploi_df[col] = None
poleemploi_df = poleemploi_df[common_cols]

# Fusionner les trois datasets
combined_df = pd.concat([aijobs_df, adzuna_df, poleemploi_df], ignore_index=True)

# Supprimer les doublons
combined_df.drop_duplicates(inplace=True)

# Export CSV combiné
output_path = os.path.join(CLEANED_DATA_PATH, "jobs_combined.csv")
combined_df.to_csv(output_path, index=False)

print(f"Données fusionnées enregistrées dans : {output_path}")
print(f"Nombre total d'offres : {len(combined_df)}")
