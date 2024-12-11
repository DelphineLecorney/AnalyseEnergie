import os
import pandas as pd
import matplotlib.pyplot as plt
import json
from matplotlib.dates import DateFormatter

def load_data(data_file):
    if not os.path.exists(data_file):
        print(f"Aucun fichier de données trouvé : {data_file}")
        return None

    data = pd.read_csv(data_file)
    required_columns = {"date", "index", "price_per_kwh", "devices", "temps"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Les colonnes nécessaires sont : {required_columns}")

    data["date"] = pd.to_datetime(data["date"])  # Convertir les dates en format datetime
    data["consumption_kwh"] = data["index"].diff().fillna(0)
    data["cost"] = data["consumption_kwh"] * data["price_per_kwh"]
    return data

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

def plot_data(data):
    weather_colors = {
        "pluie": "gray",
        "soleil": "mediumaquamarine",
        "mitigé": "darkgray",
        "gris": "dimgray"
    }
    data["color"] = data["temps"].map(weather_colors)

    fig, ax1 = plt.subplots(figsize=(10, 6))  

    bars = ax1.bar(data["date"], data["consumption_kwh"], color=data["color"], width=0.6, label="Consommation (kWh)")
    ax1.set_ylabel("Consommation (kWh)", color="black")
    ax1.tick_params(axis="y", labelcolor="black")

    for bar, (_, row) in zip(bars.patches, data.iterrows()):
        devices = row["devices"].split(", ")  # Liste des appareils
        device_text = "\n".join(devices)  # Texte à afficher
        
        # Vérifier si la barre est trop petite
        if bar.get_height() < 1:
            # Ajouter le texte au-dessus de la barre
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # Position X centrée
                bar.get_height() + 1,  # Position juste au-dessus de la barre
                device_text,
                ha="center", va="bottom", fontsize=10, color="black", fontweight="bold"
            )
        else:
            # Ajouter le texte à l'intérieur de la barre
            plt.text(
                bar.get_x() + bar.get_width() / 2,  # Position X centrée
                bar.get_height() / 2,  # Position Y à mi-hauteur
                device_text,  # Texte des appareils
                ha="center", va="bottom", fontsize=8, color="white", fontweight="bold"
            )

    
    # Axe de droite pour le coût
    ax2 = ax1.twinx()
    ax2.plot(data["date"], data["cost"], marker="o", color="teal", label="Coût quotidien (€)")
    ax2.set_ylabel("Coût (€)", color="teal")
    ax2.tick_params(axis="y", labelcolor="teal")

    # Formatage des dates
    ax1.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))

    # Ajouter une légende combinée
    weather_legend = [plt.Line2D([0], [0], color=color, lw=4) for color in weather_colors.values()]
    weather_labels = [weather.capitalize() for weather in weather_colors.keys()]
    series_legend = ax1.get_legend_handles_labels()[0] + ax2.get_legend_handles_labels()[0]
    series_labels = ["Bar consommation", "Coût quotidien (€)"]

    plt.legend(weather_legend + series_legend, weather_labels + series_labels, loc="upper left", ncol=1)
    plt.title("Consommation énergétique quotidienne avec conditions météorologiques")
    plt.tight_layout()
    plt.show()

def main():
    print("Bienvenue dans l'analyse énergétique")
    data_file = "data/energy_data.csv"
    data = load_data(data_file)
    if data is None:
        return

    save_statistics(data)
    plot_data(data)

if __name__ == "__main__":
    main()
