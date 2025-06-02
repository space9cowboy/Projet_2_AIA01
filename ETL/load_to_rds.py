import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_HOST = os.getenv("RDS_HOST")              # ex: projet-data-cloud.xxxxxx.eu-west-3.rds.amazonaws.com
DB_NAME = os.getenv("RDS_NAME")              # ex: projet-data-cloud
DB_USER = os.getenv("RDS_USER")              # ex: postgres
DB_PASSWORD = os.getenv("RDS_PASSWORD")      # ton mot de passe
DB_PORT = 5432

# Connexion à la base RDS PostgreSQL
try:
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Connexion à la base RDS réussie.")
except Exception as e:
    print("❌ Connexion échouée :", e)
    exit()

# Créer la table si elle n'existe pas
create_table_query = """
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    contract_type TEXT,
    source TEXT
);
"""
cursor.execute(create_table_query)
print("✅ Table 'jobs' vérifiée ou créée.")

# Lire le fichier CSV nettoyé
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(BASE_DIR, "data", "cleaned", "jobs_combined.csv")
df = pd.read_csv(csv_path)

# Insérer les lignes dans la base
insert_query = """
INSERT INTO jobs (title, company, location, salary_min, salary_max, contract_type, source)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    values = (
        row["title"],
        row["company"],
        row["location"],
        row["salary_min"] if not pd.isna(row["salary_min"]) else None,
        row["salary_max"] if not pd.isna(row["salary_max"]) else None,
        row["contract_type"] if not pd.isna(row["contract_type"]) else None,
        row["source"]
    )
    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        print("❌ Erreur lors de l'insertion :", e)

print(f"✅ {len(df)} lignes insérées dans la table 'jobs'.")

# Fermer la connexion
cursor.close()
conn.close()
