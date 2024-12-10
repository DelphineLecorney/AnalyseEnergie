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
    required_columns = {"date", "index", "price_per_kwh", "devices", 'temps'}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Les colonnes suivantes sont nécessaires : {required_columns}")

    # Calculer la consommation (différence entre indices)
    data["consumption_kwh"] = data["index"].diff().fillna(0)

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

    # Calculer le coût quotidien
    data["cost"] = data["consumption_kwh"] * data["price_per_kwh"]
    
    # Tracer un graphique du coût énergétique quotidien
    plt.figure(figsize=(10, 5))
    plt.plot(data["date"], data["cost"], marker="o", label="Coût quotidien (€)", color="teal")
    plt.xlabel("Date")
    plt.ylabel("Coût (€)")
    plt.title("Coût énergétique quotidien")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show(block=False)




    # Définir les couleurs en fonction des conditions météorologiques
    weather_colors = {
        "pluie": "gray",
        "soleil": "gold",
        "mitigé": "orange"
    }

    # Ajouter une colonne de couleur à chaque ligne pour uniformiser
    data["color"] = data["temps"].map(weather_colors)

    # Créer le graphique
    plt.figure(figsize=(10, 6))

    # Tracer les barres avec les couleurs définies par la météo
    bars = plt.bar(data["date"], data["consumption_kwh"], color=data["color"], width=0.6, label="Consommation quotidienne (kWh)")

    # Ajouter les noms des appareils à l'intérieur des barres
    for bar, (_, row) in zip(bars, data.iterrows()):
        # Liste des appareils à afficher
        devices = row["devices"].split(", ")  # Séparer les appareils par une virgule
        device_text = "\n".join(devices)  # Les mettre chacun sur une nouvelle ligne
        
        # Ajouter le texte des appareils à l'intérieur des barres
        plt.text(
            bar.get_x() + bar.get_width() / 2,  # Position X centrée
            bar.get_height() / 2,  # Position Y à mi-hauteur
            device_text,  # Texte des appareils
            ha="center", va="center", fontsize=8, color="white", fontweight="bold"
        )

    # Ajouter une légende pour les couleurs météo
    for weather, color in weather_colors.items():
        plt.bar(0, 0, color=color, label=f"{weather.capitalize()}")  # Barres invisibles pour la légende

    # Ajouter les labels d'axe et le titre
    plt.xlabel("Date")
    plt.ylabel("Consommation (kWh)")
    plt.title("Consommation énergétique quotidienne avec conditions météorologiques et appareils")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




if __name__ == "__main__":
    main()
