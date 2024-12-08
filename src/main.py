# src/main.py
import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    print("Bienvenue dans l'analyse énergétique")

    # Vérifier si le fichier de données existe
    data_file = os.path.join("data", "energy_data.csv")
    if not os.path.exists(data_file):
        print("Aucun fichier de données trouvé")
        return
    
    # Charger les données
    print("Chargement des données...")
    data = pd.read_csv(data_file)

    print("Aperçu des données :")
    print(data.head())

    # Moyenne de consommation
    if "consumption_kwh" in data.columns:
        avg_consumption = data["consumption_kwh"].mean()
        print(f'La consommation moyenne est de : {avg_consumption:,.2f} kwh')

    # Tracer un graphique
    plt.plot(data['date'], data["consumption_kwh"], label="Consommation")
    plt.xlabel("Date")
    plt.ylabel("Consommation (Kwh)")
    plt.title("Consommation énergétique au fil du temps")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
