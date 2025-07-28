import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from processing.data_processing import load_data
from visualization.visualization import plot_data_interactive, plot_data


def main():
    st.set_page_config(page_title="Analyse Énergétique", layout="wide")

    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "À propos"],
        icons=["bar-chart", "info-circle"],
        orientation="horizontal",
        default_index=0,
    )

    if selected == "Dashboard":
        st.title("⚡ Dashboard - Analyse énergétique")

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
            st.error(" Les données sont vides ou mal formatées.")
            return


        # Filtres
        with st.expander("🔧 Filtres avancés (cliquer pour développer)", expanded=True):
            col_date, col_weather = st.columns(2)

            # 🎯 Filtrage par date
            with col_date:
                st.subheader("📅 Filtrer par période")
                start_date = st.date_input("Date de début", data["date"].min().date())
                end_date = st.date_input("Date de fin", data["date"].max().date())

            # 🌦️ Filtrage météo
            with col_weather:
                st.subheader("🌤️ Filtrer par météo")
                weather_options = data["temps"].dropna().unique()
                selected_weather = st.multiselect("Types de météo :", weather_options)
                
        data = data[(data["date"] >= pd.to_datetime(start_date)) & (data["date"] <= pd.to_datetime(end_date))]

        if selected_weather:
                    data = data[data["temps"].isin(selected_weather)]

        # 🔍 Aperçu
        st.subheader("🔍 Aperçu des données filtrées")
        st.dataframe(data.head())

        # Onglets : Statistiques / Graphiques
        tab1, tab2 = st.tabs(["📊 Statistiques", "📈 Visualisation"])

        with tab1:
            # 📊 Statistiques
            st.subheader("📊 Statistiques clés")
            col1, col2, col3 = st.columns(3)
            col1.metric("Consommation totale (kWh)", f"{data['consumption_kwh'].sum():.2f}")
            col2.metric("Coût total (€)", f"{data['cost'].sum():.2f}")
            col3.metric("Nombre de jours", data['date'].nunique())
        with tab2:
            # 📈 Graphique
            st.subheader("📉 Visualisation")
            plot_type = st.selectbox("Type de graphique", ["Statique (matplotlib)", "Interactif (Plotly)"])
            if st.button("🎨 Afficher le graphique"):
                if plot_type == "Statique (matplotlib)":
                    plot_data(data, in_streamlit=True)
                else:
                    plot_data_interactive(data)

    elif selected == "À propos":
        st.markdown("## À propos du projet")
        st.markdown("Ce dashboard visualise les données de consommation énergétique avec filtres, stats et graphes.")


if __name__ == "__main__":
    main()
