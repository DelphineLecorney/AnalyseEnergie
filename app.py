import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

import streamlit as st
import pandas as pd
from processing.data_processing import load_data
from visualization.visualization import plot_data_interactive, plot_data

def main():
    st.title("Dashboard - Analyse énergétique")

    uploaded_file = st.file_uploader("Charger un fichier CSV (facultatif)", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_raw.to_csv("data/temp_uploaded.csv", index=False)
        data = load_data("data/temp_uploaded.csv")
        st.success("Fichier chargé avec succès.")
    else:
        default_path = "data/energy_data.csv"
        st.warning(f"Aucun fichier chargé. Utilisation du fichier par défaut : `{default_path}`")
        data = load_data(default_path)

    # Aperçu des données
    st.subheader("🔍 Aperçu des données")
    st.dataframe(data.head())

    # Choix du graphique
    plot_type = st.selectbox("Type de graphique", ["Statique (matplotlib)", "Interactif (Plotly)"])

    if st.button("Afficher le graphique"):
        if plot_type == "Statique (matplotlib)":
            plot_data(data, in_streamlit=True)
        else:
            plot_data_interactive(data)


if __name__ == "__main__":
    main()
