import os
import json

def save_statistics(data, output_dir="data"):
    avg_consumption = data["consumption_kwh"].mean()
    max_consumption = data["consumption_kwh"].max()
    min_consumption = data["consumption_kwh"].min()
    total_cost = data["cost"].sum()

    stats = {
        "Moyenne consommation (kWh)": avg_consumption,
        "Max consommation (kWh)": max_consumption,
        "Min consommation (kWh)": min_consumption,
        "Coût total (€)": total_cost,
    }
    stats_file = os.path.join(output_dir, "statistics.json")
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=4)
    print(f"Statistiques sauvegardées dans : {stats_file}")
    print("Aperçu des données :")
    print(data.head())
