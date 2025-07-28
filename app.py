import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
import pandas as pd
from processing.data_processing import load_data
from visualization.visualization import plot_data_interactive, plot_data

def main():
    st.set_page_config(page_title="Analyse Énergétique", layout="wide")
    st.title("⚡ Dashboard - Analyse énergétique")

    # 📁 Chargement du fichier CSV
    uploaded_file = st.file_uploader("📄 Charger un fichier CSV (facultatif)", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_raw.to_csv("data/temp_uploaded.csv", index=False)
        data = load_data("data/temp_uploaded.csv")
        st.success("Fichier chargé avec succès.")
    else:
        default_path = "data/energy_data.csv"
        st.warning(f"Aucun fichier chargé. Utilisation du fichier par défaut : `{default_path}`")
        data = load_data(default_path)

    if data is None or data.empty:
        st.error("Les données sont vides ou mal formatées.")
        return

    # Filtrage par date
    st.subheader("📅 Filtrer par période")
    start_date = st.date_input("Date de début", data["date"].min().date())
    end_date = st.date_input("Date de fin", data["date"].max().date())

    data = data[(data["date"] >= pd.to_datetime(start_date)) & (data["date"] <= pd.to_datetime(end_date))]

    # Filtrage par météo
    st.subheader("🌤️ Filtrer par météo")
    weather_options = data["temps"].dropna().unique()
    selected_weather = st.multiselect("Choisissez le ou les types de météo :", weather_options)

    if selected_weather:
        data = data[data["temps"].isin(selected_weather)]

    #  Aperçu des données
    st.subheader("🔍 Aperçu des données filtrées")
    st.dataframe(data.head())

    # Statistiques
    st.subheader("📊 Statistiques clés")
    col1, col2, col3 = st.columns(3)
    col1.metric("Consommation totale (kWh)", f"{data['consumption_kwh'].sum():.2f}")
    col2.metric("Coût total (€)", f"{data['cost'].sum():.2f}")
    col3.metric("Nombre de jours", data["date"].nunique())

    # 📈 Choix de type de graphique
    plot_type = st.selectbox("📉 Type de graphique", ["Statique (matplotlib)", "Interactif (Plotly)"])

    if st.button("🎨 Afficher le graphique"):
        if plot_type == "Statique (matplotlib)":
            plot_data(data, in_streamlit=True)
        else:
            plot_data_interactive(data)

if __name__ == "__main__":
    main()
