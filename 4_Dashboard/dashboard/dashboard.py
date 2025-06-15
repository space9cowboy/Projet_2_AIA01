# Dashboard interactif Streamlit pour l'analyse des offres d'emploi Data Science

import os
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Dashboard Emploi Data Science", layout="wide")

# === Chargement des variables d'environnement ===
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# === Connexion à la base de données RDS ===
@st.cache_data(ttl=600)
def load_data():
    try:
        engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
        df = pd.read_sql("SELECT * FROM jobs", con=engine)
        return df
    except Exception as e:
        st.error("Erreur de connexion à la base RDS : " + str(e))
        return pd.DataFrame()

# === Chargement des données ===
# Nettoyage des valeurs dans la colonne 'source'
def normalize_sources(df):
    df["source"] = df["source"].astype(str).str.strip().str.lower()
    df["source"] = df["source"].replace({
        "ai-jobs.net": "AI Jobs",
        "ai jobs": "AI Jobs",
        "aijobs": "AI Jobs",
        "adzuna": "Adzuna",
        "api adzuna": "Adzuna",
        "pole emploi": "Pôle Emploi",
        "pôle emploi": "Pôle Emploi",
        "api pole emploi": "Pôle Emploi"
    })
    df["source"] = df["source"].str.title()  # Standardiser le casing
    return df
df = normalize_sources(load_data())

# === Sidebar - Roadmap du projet ===
with st.sidebar.expander("📆 Roadmap du projet", expanded=False):
    st.markdown("""
- ✅ Collecte des données (AI-jobs.net, Adzuna, API Pôle Emploi)
- ✅ Nettoyage, normalisation et fusion des jeux de données
- ✅ Stockage sur AWS (PostgreSQL via RDS, fichiers bruts sur S3)
- ✅ Création du notebook d’analyse exploratoire (Seaborn, Matplotlib, Pandas)
- ✅ Conception du dashboard interactif avec Streamlit
- ✅ Intégration des visualisations dynamiques (Plotly, Folium)
- ✅ Ajout des métriques, KPIs, visualisations croisées
- 🔄 Optimisation du design UI (onglets, filtres, layout)
- 🔜 Ajout de filtres dynamiques avancés & carte interactive
- 🚀 Mise en production prévue (Docker, GitHub Actions, hébergement Cloud)
""")

    # === Insights dans la sidebar ===
with st.sidebar.expander(" 📈 Insights Important", expanded=False):
    st.markdown("""
---
### © Insights clés
""")
    try:
        df["has_salary"] = df["salary_min"].notnull() & df["salary_max"].notnull()
        st.markdown(f"- 🔍 **Source dominante** : {df['source'].value_counts().idxmax()}")
        st.markdown(f"- 💰 **Offres avec salaire** : {len(df[df['has_salary']])}")
        st.markdown(f"- 📊 **Total d'offres** : {len(df)}")
        st.markdown(f"- 🏢 **Entreprises uniques** : {df['company'].nunique()}")
        st.markdown(f"- 🌍 **Villes uniques** : {df['location'].nunique()}")
        st.markdown(f"- 🧑‍💻 **Poste le + fréquent** : {df['title'].mode()[0]}")
        st.markdown(f"- 🏭 **Entreprise la + active** : {df['company'].value_counts().idxmax()}")
        st.markdown(f"- 💸 **Salaire max moyen** : {df['salary_max'].dropna().mean():.0f} €")
        st.markdown(f"- 💸 **Salaire min médian** : {df['salary_min'].dropna().median():.0f} €")
        st.markdown(f"- 📈 **% avec salaire** : {df['has_salary'].mean() * 100:.2f}%")
        st.markdown(f"- 🧾 **Postes uniques** : {df['title'].nunique()}")
    except:
        st.warning("Impossible de générer les insights.")
    # === Code source GitHub ===
    st.markdown("""
---
### 📁 Code source :
- [Lien GitHub du projet](https://github.com/space9cowboy/Projet_2_AIA01)
""")

if not df.empty:
    df.dropna(subset=["title", "company", "location"], inplace=True)
    df["title"] = df["title"].str.lower().str.strip()
    df["company"] = df["company"].str.strip()
    df["location"] = df["location"].str.strip()

    st.title("📊 Dashboard Emploi Data Science")
    st.markdown("Explorez les tendances de recrutement en Data Science en France via les données collectées.")

     # Onglets
    tab1, tab2, tab3, tab4, tab6, tab7, tab8 = st.tabs([
        "Sources",
        "Localisations",
        "Postes",
        "Salaires",
        "Croisement",
        "Entreprise",
        "A Propos"
    ])

    with tab1:
        st.subheader("🌐 Nombre d'annonces par source")
        source_counts = df["source"].value_counts().reset_index()
        source_counts.columns = ["source", "count"]

        # Bar chart
        fig1 = px.bar(source_counts, x="source", y="count",
                      labels={"source": "Source", "count": "Nombre d'annonces"}, color_discrete_sequence=["#4C78A8"])
        st.plotly_chart(fig1)

        # Pie chart
        fig_pie = px.pie(source_counts, names="source", values="count", title="Origine des offres (API vs Scraping)", hole=0.3)
        st.plotly_chart(fig_pie)

        st.info(f"🔍 Les {len(source_counts)} sources affichées regroupent {source_counts['count'].sum()} offres, soit environ {round(100 * source_counts['count'].sum() / len(df))}% des annonces filtrées.")
        st.info("ℹ️ Ces graphiques permettent de comparer les canaux de diffusion des annonces collectées (scraping vs APIs).")

    with tab2:
        st.subheader("📍 Répartition des offres par ville (Top 15)")
        df_city = df["location"].value_counts().head(30).reset_index()
        df_city.columns = ["city", "count"]
        fig_city = px.bar(df_city, x="city", y="count", title="Top 15 des villes avec le plus d'offres",
                          labels={"city": "Ville", "count": "Nombre d'offres"}, color_discrete_sequence=["#FF6F61"])
        st.plotly_chart(fig_city)
        st.info(f"🔎 Les {len(df_city)} premières villes regroupent {df_city['count'].sum()} offres, soit environ {round(100 * df_city['count'].sum() / len(df))}% des annonces filtrées.")

    with tab3:
        st.subheader("Postes les plus fréquents")
        top_titles = df["title"].value_counts().head(30).reset_index()
        top_titles.columns = ["title", "count"]
        fig3 = px.bar(top_titles, x="count", y="title", orientation="h",
                      labels={"title": "Poste", "count": "Nombre"}, color_discrete_sequence=["#54A24B"])
        st.plotly_chart(fig3)
        st.info("ℹ️ Cette visualisation révèle les métiers les plus demandés (Data Scientist, Analyste, etc.).")
        
        st.subheader("📄 Répartition des types de contrats")
        fig_contract, ax_contract = plt.subplots(figsize=(8, 5))
        sns.countplot(data=df, y="contract_type", order=df["contract_type"].value_counts().index, palette="pastel", ax=ax_contract)
        ax_contract.set_title("Répartition des types de contrats")
        ax_contract.set_xlabel("Nombre d'offres")
        st.pyplot(fig_contract)

        total_contracts = df["contract_type"].notna().sum()
        top_contracts = df["contract_type"].value_counts().head(3)
        st.info(f"📊 Sur {total_contracts} offres renseignées, les types de contrats les plus fréquents sont :\n" + \
                "\n".join([f"- {ct}: {count} offres ({count / total_contracts * 100:.1f}%)" for ct, count in top_contracts.items()]))
        
        if "category" in df.columns:
            st.subheader("📁 Répartition des catégories d'emploi")
            fig_cat, ax_cat = plt.subplots(figsize=(8, 5))
            df["category"].value_counts().head(10).plot(kind="barh", color="lightgreen", ax=ax_cat)
            ax_cat.set_title("Top 10 des catégories d'emploi")
            ax_cat.set_xlabel("Nombre d'offres")
            st.pyplot(fig_cat)

        total_cat = df["category"].notna().sum()
        top_cats = df["category"].value_counts().head(3)
        st.info(f"📌 Sur {total_cat} offres catégorisées, les plus fréquentes sont :\n" + \
                "\n".join([f"- {cat}: {count} offres ({count / total_cat * 100:.1f}%)" for cat, count in top_cats.items()]))

    with tab4:
        st.subheader("Distribution des salaires")

        if "salary_min" in df.columns and "salary_max" in df.columns:
            fig4 = px.histogram(df, x=df["salary_max"], nbins=30, title="Distribution des salaires max", color_discrete_sequence=["#E45756"])
            st.plotly_chart(fig4)
            st.info("ℹ️ Cette courbe montre la répartition des salaires max. Elle permet d’identifier les seuils de rémunération les plus fréquents.")


            df_salaire = df.dropna(subset=["salary_min", "salary_max"])
            fig_box = px.box(df_salaire, y="salary_max", points="all", title="Distribution des salaires max", color_discrete_sequence=["#59C3C3"])
            st.plotly_chart(fig_box)
            moyenne = int(df_salaire["salary_max"].mean())
            mediane = int(df_salaire["salary_max"].median())
            max_val = int(df_salaire["salary_max"].max())
            st.info(f"📊 Salaire max moyen : {moyenne} € — Médiane : {mediane} € — Maximum observé : {max_val} €")
            
            df["has_salary"] = df["salary_min"].notnull() & df["salary_max"].notnull()
            salary_counts = df["has_salary"].value_counts().rename({True: "Avec salaire", False: "Sans salaire"})
            fig7 = px.pie(values=salary_counts.values, names=salary_counts.index, title="Présence des salaires dans les offres")
            st.plotly_chart(fig7)
            st.info(f"📊 Environ {salary_counts['Avec salaire']} offres ({round(100 * salary_counts['Avec salaire'] / salary_counts.sum(), 1)}%) contiennent une information salariale, contre {salary_counts['Sans salaire']} offres ({round(100 * salary_counts['Sans salaire'] / salary_counts.sum(), 1)}%) sans indication de salaire.")

            
        else:
            st.warning("⚠️ Colonne 'salary' non disponible.")
        
        # === Statistiques descriptives sur les salaires ===
        st.subheader("📊 Statistiques descriptives sur les salaires")
        if "salary_min" in df.columns and "salary_max" in df.columns:
            desc_min = df["salary_min"].describe()
            desc_max = df["salary_max"].describe()

            st.markdown("**Statistiques sur `salary_min` :**")
            st.markdown(f"- Moyenne : {desc_min['mean']:.2f} €")
            st.markdown(f"- Médiane : {desc_min['50%']:.2f} €")
            st.markdown(f"- Min : {desc_min['min']:.2f} € — Max : {desc_min['max']:.2f} €")
            st.markdown(f"- Écart-type : {desc_min['std']:.2f} €")

            st.markdown("**Statistiques sur `salary_max` :**")
            st.markdown(f"- Moyenne : {desc_max['mean']:.2f} €")
            st.markdown(f"- Médiane : {desc_max['50%']:.2f} €")
            st.markdown(f"- Min : {desc_max['min']:.2f} € — Max : {desc_max['max']:.2f} €")
            st.markdown(f"- Écart-type : {desc_max['std']:.2f} €")
        else:
            st.warning("⚠️ Colonnes 'salary_min' ou 'salary_max' manquantes dans le dataset.")


    with tab6:
        st.subheader("🗺️ Croisement : Localisations vs Postes")
        top_locations = df["location"].value_counts().head(5).index
        top_titles = df["title"].value_counts().head(5).index
        heatmap_data = df[df["location"].isin(top_locations) & df["title"].isin(top_titles)]
        pivot = pd.crosstab(heatmap_data["location"], heatmap_data["title"])
        fig6, ax6 = plt.subplots(figsize=(10, 6))
        sns.heatmap(pivot, annot=True, cmap="YlGnBu", fmt="d", ax=ax6)
        st.pyplot(fig6)

        total_heatmap = pivot.values.sum()
        st.info(
            f"🔍 Cette heatmap montre la répartition croisée des postes et localisations les plus populaires. "
            f"Au total, **{total_heatmap}** offres concernent les 5 postes et les 5 villes les plus représentées."
        )

    with tab7:
        st.subheader("🏢 Entreprises qui recrutent le plus")

        df_company = df["company"].value_counts().head(15).reset_index()
        df_company.columns = ["company", "count"]

        # Exemple 1 : Pie Chart
        fig_pie = px.pie(df_company, names="company", values="count", title="Top 15 des entreprises qui recrutent", hole=0.3)
        st.plotly_chart(fig_pie)

        # Exemple 2 : Bar Chart
        fig_bar = px.bar(df_company, x="company", y="count", title="Volume d'offres par entreprise (Top 15)", color_discrete_sequence=["#33C3F0"])
        st.plotly_chart(fig_bar)

        # Exemple 3 : Histogramme vertical
        fig_hist = px.histogram(df_company, x="company", y="count", title="Histogramme des entreprises actives", color_discrete_sequence=["#FAA43A"])
        st.plotly_chart(fig_hist)

        total_offres = df_company["count"].sum()
        pourcentage = round((total_offres / len(df)) * 100, 1)
        st.info(f"🔍 Les 15 entreprises les plus actives représentent {total_offres} offres, soit environ {pourcentage}% des annonces filtrées.")
        
    with tab8:
        st.header("À propos du projet")
        st.markdown("""
            **🎯 Objectif du projet :**  
            Ce dashboard permet de visualiser les données issues d’un pipeline complet de collecte d’offres d’emploi dans la Data (scraping & APIs), transformées et stockées sur AWS RDS, puis explorées avec Python.

            **🗂 Sources de données :**  
            - `ai-jobs.net` (scraping avec BeautifulSoup)  
            - `API Adzuna`  
            - `API Pôle Emploi`

            **🔧 Pipeline ETL :**  
            - Scripts de collecte → Nettoyage → Stockage sur PostgreSQL (via SQLAlchemy) et AWS S3

            **📁 Données stockées :**  
            - Intitulé (`title`), entreprise, lieu, salaires min/max, type de contrat, date, source

            **📊 Analyses intégrées :**  
            - Volume d’annonces par source / localisation / entreprise / poste  
            - Répartition temporelle des publications  
            - Distribution des salaires et outliers (boxplot, histogrammes)  

            **🌐 Stack utilisée :**  
            - Python (Streamlit, Pandas, Seaborn, Plotly, SQLAlchemy)  
            - PostgreSQL sur AWS RDS, AWS S3

            **📁 Code source :**  
            - [Lien GitHub du projet](https://github.com/ton-utilisateur/projet-data-cloud)
            """)
else:
    st.warning("⚠️ Impossible de charger les données.")
