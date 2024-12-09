# src/main.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import json

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
        max_consumption = data["consumption_kwh"].max()
        min_consumption = data["consumption_kwh"].min()
        total_cost = (data["consumption_kwh"] * data["price_per_kwh"]).sum()

        print(f'La consommation moyenne est de : {avg_consumption:,.2f} kwh')
        print(f'La consommation maximale est de : {max_consumption:,.2f} kwh')
        print(f'La consommation minimale est de : {min_consumption:,.2f} kwh')
        print(f'Le coût total de l\énergie consommée est de : {total_cost:,.2f} €')

    # liste ou description d'appareils)
    if "devices" in data.columns:
        # Assurez-vous que la colonne n'a pas de valeurs manquantes
        if data["devices"].isnull().any():
            print("Attention : Certaines lignes de la colonne 'devices' sont vides.")
        
        # Extraire les appareils et afficher les informations
        device_list = data["devices"].dropna().unique()  # Liste unique des appareils
        print("Liste des appareils :", device_list)
    else:
        print("La colonne 'devices' n'existe pas dans les données.")
        device_list = []  # Liste vide si la colonne n'existe pas


    # Résultats statistiques
    stats = {
        "Moyenne consommation (Kwh)": avg_consumption,
        "Max consommation (Kwh)": max_consumption,
        "Min consommation (Kwh)": min_consumption,
        "Coût total (€)": total_cost
    }

    # Créer une structure avec les dates et appareils
    device_info = {
        "Appareils par date": [
            {"date": row["date"], "appareils": row.get("devices", "N/A")} 
            for _, row in data.iterrows()
        ]
    }

    # Sauvegarder les statistiques dans un fichier CSV
    stats_df = pd.DataFrame([stats])
    stats_file = os.path.join("data", "statistics_.csv")
    stats_df.to_csv(stats_file, index=False)
    print(f"Les statistiques ont été sauvegardées dans {stats_file}")

    # Sauvegarder les informations sur les appareils dans un fichier JSON
    devices_file = os.path.join("data", "devices_info.json")
    with open(devices_file, 'w') as f:
        json.dump(device_info, f, indent=4)
    print(f"Les informations sur les appareils ont été sauvegardées dans {devices_file}")

    # Tracer un graphique
    plt.plot(data['date'], data["consumption_kwh"], label="Consommation")
    plt.xlabel("Date")
    plt.ylabel("Consommation (Kwh)")
    plt.title("Consommation énergétique au fil du temps")
    plt.legend()
    plt.show(block=False)

    # Tracer un deuxième graphique
    data['cost'] = data['consumption_kwh'] * data['price_per_kwh']
    plt.figure(figsize=(10, 6))
    plt.bar(data['date'], data['cost'], color='mediumaquamarine', label="Coût quotidien (€)")
    for i, row in data.iterrows():
        plt.text(row['date'], row['cost'], row.get('devices', 'N/A'), ha='center', fontsize=8, rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Coût (€)")
    plt.title("Coût quotidien de l'énergie consommée")
    plt.legend()
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    main()
