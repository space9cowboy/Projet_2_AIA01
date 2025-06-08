# 📁 Script/Documentation de création de l’instance RDS PostgreSQL sur AWS

Ce document fournit les instructions pour créer une base de données relationnelle PostgreSQL avec AWS RDS, à l’aide de l’interface graphique de la console AWS.

---

## Prérequis
- Un compte AWS actif
- Des droits suffisants pour accéder à RDS
- Une paire de clés IAM 

---

## Étapes via la console AWS

### 1. Accéder à AWS RDS
- Se rendre sur [https://console.aws.amazon.com/rds](https://console.aws.amazon.com/rds)
- Cliquez sur **Create database**

### 2. Sélectionner les options
- **Engine** : PostgreSQL
- **Version** : choisir la plus récente stable (15.5 ou 14.10)
- **Template** : Free tier (si disponible)

### 3. Créer les identifiants de connexion
- **DB instance identifier** : `projet-data-cloud`
- **Master username** : `admin`
- **Master password** : (ex) `Sljndfljkbmfk7hk9`

### 4. Configuration de stockage et accès
- **Public access** : `Yes` (si on souhaitez accéder à la base depuis l’externe)
- **VPC Security group** : Créer un nouveau ou en utiliser un existant avec le port `5432` ouvert

### 5. Création
- Cliquez sur **Create database**
- On patiente quelques minutes jusqu'à ce que le statut devienne "Available"

---

## Connexion à la base

- J'ai utilisé un script Python avec `psycopg2` mais on peut aussi utiliser `sqlalchemy`

**Données de connexion :**
```
Hôte        : projet-data-cloud.xxxxxx.eu-west-3.rds.amazonaws.com
Port        : 5432
Utilisateur : admin
Mot de passe: Sljndfljkbmfk7hk9
Base        : projet-data-cloud
```

---

## Conseils de sécurité
- Ne jamais exposer nos identifiants dans le code
- On doit utiliser le `.env` ou AWS Secrets Manager pour stocker nos variables sensibles

---

##  Script Python de test de connexion
```python
import psycopg2

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
    print("Connexion à la base RDS réussie.")
except Exception as e:
    print("Connexion échouée :", e)
    exit(1)
```

---

