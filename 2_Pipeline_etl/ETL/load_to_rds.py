import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

DB_HOST = os.getenv("RDS_HOST")
DB_NAME = os.getenv("RDS_NAME")
DB_USER = os.getenv("RDS_USER")
DB_PASSWORD = os.getenv("RDS_PASSWORD")
DB_PORT = 5432

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
    exit(1)

# Créer la table avec toutes les colonnes utiles
create_table_query = """
CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    company TEXT,
    location TEXT,
    salary_min NUMERIC,
    salary_max NUMERIC,
    contract_type TEXT,
    description TEXT,
    created TIMESTAMP,
    category TEXT,
    source TEXT
);
"""
cursor.execute(create_table_query)
print("📦 Table 'jobs' vérifiée ou créée.")

# Lire le fichier CSV nettoyé
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
csv_path = os.path.join(BASE_DIR, "data", "cleaned", "jobs_combined.csv")

try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print("❌ Fichier introuvable :", csv_path)
    cursor.close()
    conn.close()
    exit(1)

# Conversion de la colonne "created" si présente
if "created" in df.columns:
    df["created"] = pd.to_datetime(df["created"], errors="coerce")

# Requête d'insertion
insert_query = """
INSERT INTO jobs (title, company, location, salary_min, salary_max, contract_type, description, created, category, source)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

inserted = 0
for _, row in df.iterrows():
    values = (
        row.get("title"),
        row.get("company"),
        row.get("location"),
        row.get("salary_min") if pd.notna(row.get("salary_min")) else None,
        row.get("salary_max") if pd.notna(row.get("salary_max")) else None,
        row.get("contract_type") if pd.notna(row.get("contract_type")) else None,
        row.get("description") if pd.notna(row.get("description")) else None,
        row.get("created") if pd.notna(row.get("created")) else None,
        row.get("category") if pd.notna(row.get("category")) else None,
        row.get("source")
    )
    try:
        cursor.execute(insert_query, values)
        inserted += 1
    except Exception as e:
        print("⚠️ Erreur lors de l'insertion :", e)

print(f"✅ {inserted} lignes insérées dans la table 'jobs'.")

# Fermer la connexion
cursor.close()
conn.close()
