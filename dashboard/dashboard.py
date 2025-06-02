import os
import pandas as pd
import streamlit as st
import plotly.express as px
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

if df.empty:
    st.warning("Aucune donnée chargée.")
    st.stop()

# === Filtres interactifs ===
ville = st.selectbox("\U0001F4CD Filtrer par ville", options=["Toutes"] + sorted(df["location"].unique().tolist()))
entreprise = st.selectbox("\U0001F3E2 Filtrer par entreprise", options=["Toutes"] + sorted(df["company"].unique().tolist()))

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
    st.subheader("\U0001F4B0 Distribution des salaires max")
    fig3 = px.box(df_filtered, y="salary_max", points="all", title="Boxplot des salaires max")
    st.plotly_chart(fig3)

# === Table des données ===
st.subheader("\U0001F4CB Aperçu des données")
st.dataframe(df_filtered.head(50))
