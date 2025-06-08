import os
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv

# === Chargement des variables d'environnement ===
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# === Connexion à la base PostgreSQL RDS ===
@st.cache_data
def load_data():
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        df = pd.read_sql("SELECT * FROM jobs", con=engine)
        df.dropna(subset=["title", "company", "location"], inplace=True)
        df["title"] = df["title"].str.lower().str.strip()
        df["company"] = df["company"].str.strip()
        df["location"] = df["location"].str.strip()
        return df
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données : {e}")
        return pd.DataFrame()

df = load_data()

# === Interface Streamlit ===
st.title("\U0001F4CA Dashboard interactif - Offres d’emploi Data")

# === Sidebar - À propos du projet ===
with st.sidebar.expander("\U0001F4D8 À propos du projet", expanded=False):
    st.markdown("""
**🎯 Objectif du projet :**  
Ce projet vise à collecter, analyser et visualiser les offres d’emploi dans le domaine de la **Data** à partir de sources en ligne (scraping et API).

**🗂 Sources de données :**  
- `ai-jobs.net` (scraping)  
- `Adzuna API`

**🔧 Pipeline ETL :**  
- Collecte ➡️ Transformation ➡️ Chargement vers AWS RDS

**📁 Données récupérées :**
- `title`, `company`, `location`, `salary_min`, `salary_max`, `contract_type`, `source`

**📊 Visualisations issues du notebook :**
- Statistiques descriptives sur les salaires
- Boxplots pour détection de valeurs extrêmes
- Histogrammes et distributions
- Corrélation entre salaires min / max
- Outliers détectés automatiquement

**🌐 Stack utilisée :**  
- Python, Streamlit, Pandas, Seaborn, Matplotlib, Plotly  
- PostgreSQL (AWS RDS), AWS S3

**📁 Code source :**  
- [Lien GitHub du projet](https://github.com/ton-utilisateur/projet-data-cloud)
""")

# === Sidebar - Roadmap du projet ===
with st.sidebar.expander("\U0001F4C6 Roadmap du projet", expanded=False):
    st.markdown("""
- ✅ Collecte des données (AI-jobs.net, Adzuna)
- ✅ Nettoyage et fusion dans jobs_combined.csv
- ✅ Chargement dans PostgreSQL via RDS
- ✅ Visualisations avec Streamlit
- ✅ Intégration des analyses du notebook (Seaborn, Matplotlib)
- 🚀 Automatisation & déploiement complet
""")

if df.empty:
    st.warning("Aucune donnée chargée.")
    st.stop()

# === Filtres interactifs ===
st.sidebar.header("\U0001F50D Filtres")
ville = st.sidebar.selectbox("\U0001F4CD Ville", options=["Toutes"] + sorted(df["location"].unique().tolist()))
entreprise = st.sidebar.selectbox("\U0001F3E2 Entreprise", options=["Toutes"] + sorted(df["company"].unique().tolist()))

df_filtered = df.copy()
if ville != "Toutes":
    df_filtered = df_filtered[df_filtered["location"] == ville]
if entreprise != "Toutes":
    df_filtered = df_filtered[df_filtered["company"] == entreprise]

# === KPIs ===
st.subheader("\U0001F4C8 Statistiques clés")
col1, col2, col3 = st.columns(3)
col1.metric("Total offres", len(df_filtered))
col2.metric("Postes uniques", df_filtered["title"].nunique())
col3.metric("Entreprises", df_filtered["company"].nunique())

# === Graphiques ===
st.subheader("\U0001F3D9️ Répartition des offres par ville")
top_cities = df_filtered["location"].value_counts().nlargest(10).reset_index()
top_cities.columns = ["Ville", "Nombre d’offres"]
fig1 = px.bar(top_cities, x="Ville", y="Nombre d’offres", title="Top 10 villes par nombre d’offres")
st.plotly_chart(fig1)

st.subheader("\U0001F4BC Entreprises les plus actives")
top_companies = df_filtered["company"].value_counts().nlargest(10).reset_index()
top_companies.columns = ["Entreprise", "Nombre d’offres"]
fig2 = px.pie(top_companies, names="Entreprise", values="Nombre d’offres", hole=0.4)
st.plotly_chart(fig2)

if "salary_max" in df_filtered.columns and df_filtered["salary_max"].notna().sum() > 0:
    st.subheader("\U0001F4B0 Distribution des salaires max (boxplot)")
    fig3 = px.box(df_filtered, y="salary_max", points="all", title="Boxplot des salaires max")
    st.plotly_chart(fig3)

    st.subheader("\U0001F4C9 Histogramme des salaires max")
    fig4, ax = plt.subplots()
    sns.histplot(df_filtered["salary_max"].dropna(), kde=True, bins=30, ax=ax)
    st.pyplot(fig4)

    st.subheader("\U0001F9EA Valeurs extrêmes détectées")
    q3 = df_filtered["salary_max"].quantile(0.75)
    iqr = q3 - df_filtered["salary_max"].quantile(0.25)
    seuil = q3 + 1.5 * iqr
    outliers = df_filtered[df_filtered["salary_max"] > seuil]
    st.dataframe(outliers)

# === Insights ===
st.subheader("\U0001F4AC Quelques insights à retenir")
nb_remote = df_filtered[df_filtered["location"].str.lower().str.contains("remote")].shape[0]
nb_contrats = df_filtered["contract_type"].nunique(dropna=True)
sal_moy = df_filtered["salary_max"].mean()

st.markdown(f"- 🌍 **Nombre d’offres en remote** : {nb_remote}")
st.markdown(f"- 📄 **Types de contrat différents** : {nb_contrats}")
st.markdown(f"- 💸 **Salaire max moyen** : {sal_moy:,.2f} €")

# === Table des données ===
st.subheader("\U0001F4CB Aperçu des données")
st.dataframe(df_filtered.head(100))
