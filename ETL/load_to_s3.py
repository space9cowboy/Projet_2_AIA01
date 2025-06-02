import boto3
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")

# Initialiser le client S3
s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Chemin du fichier local
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "data", "cleaned", "jobs_combined.csv")
s3_key = "jobs/jobs_combined.csv"  # Dossier virtuel dans le bucket

try:
    s3.upload_file(file_path, S3_BUCKET, s3_key)
    print(f"Fichier uploadé avec succès dans s3://{S3_BUCKET}/{s3_key}")
except Exception as e:
    print("Erreur lors de l'upload :", e)
