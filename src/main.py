import os
import pandas as pd
import matplotlib.pyplot as plt
import json

def main():
    print("Bienvenue dans l'analyse énergétique")

    # Chemin du fichier de données
    data_file = "data/energy_data.csv"

    # Vérifier l'existence du fichier
    if not os.path.exists(data_file):
        print(f"Aucun fichier de données trouvé : {data_file}")
        return

    # Charger les données
    data = pd.read_csv(data_file)

    # Vérifier si les colonnes nécessaires sont présentes
    required_columns = {"date", "index", "price_per_kwh", "devices"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Les colonnes suivantes sont nécessaires : {required_columns}")

    # Calculer la consommation (différence entre indices)
    data["consumption_kwh"] = data["index"].diff().fillna(0)
    data["consumption_kwh"] = data["consumption_kwh"].clip(lower=0)  # Éviter les valeurs négatives

    # Sauvegarder les données mises à jour dans le fichier CSV
    output_file = "data/updated_energy.csv"
    data.to_csv(output_file, index=False)
    print(f"Données mises à jour sauvegardées dans : {output_file}")

    # Afficher un aperçu des données
    print("Aperçu des données :")
    print(data.head())

    # Calculs statistiques
    avg_consumption = data["consumption_kwh"].mean()
    max_consumption = data["consumption_kwh"].max()
    min_consumption = data["consumption_kwh"].min()
    total_cost = (data["consumption_kwh"] * data["price_per_kwh"]).sum()

    print(f"Consommation moyenne : {avg_consumption:.2f} kWh")
    print(f"Consommation maximale : {max_consumption:.2f} kWh")
    print(f"Consommation minimale : {min_consumption:.2f} kWh")
    print(f"Coût total : {total_cost:.2f} €")

    # Sauvegarder les statistiques dans un fichier JSON
    stats = {
        "Moyenne consommation (kWh)": avg_consumption,
        "Max consommation (kWh)": max_consumption,
        "Min consommation (kWh)": min_consumption,
        "Coût total (€)": total_cost,
    }
    stats_file = "data/statistics.json"
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=4)
    print(f"Statistiques sauvegardées dans : {stats_file}")

    # Tracer un graphique de la consommation
    plt.figure(figsize=(10, 5))
    plt.plot(data["date"], data["consumption_kwh"], marker="o", label="Consommation (kWh)")
    plt.xlabel("Date")
    plt.ylabel("Consommation (kWh)")
    plt.title("Consommation énergétique journalière")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show(block=False)

    # Tracer un graphique du coût quotidien
    data["cost"] = data["consumption_kwh"] * data["price_per_kwh"]
    plt.figure(figsize=(10, 5))
    plt.bar(data["date"], data["cost"], color="mediumaquamarine", label="Coût quotidien (€)")
    for i, row in data.iterrows():
        plt.text(row['date'], row['cost'], row.get('devices', 'N/A'), ha='center', fontsize=8, rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Coût (€)")
    plt.title("Coût énergétique quotidien")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
