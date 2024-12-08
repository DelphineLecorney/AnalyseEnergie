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

    # Moyenne, min, max, .. de consommation
    if "consumption_kwh" in data.columns:
        avg_consumption = data["consumption_kwh"].mean()
        max_consumption = data["consumption_kwh"].max()
        min_consumption = data["consumption_kwh"].min()
        total_cost = (data["consumption_kwh"] * data["price_per_kwh"]).sum()

        print(f'La consommation moyenne est de : {avg_consumption:,.2f} kwh')
        print(f'La consommation maximale est de : {max_consumption:,.2f} kwh')
        print(f'La consommation minimale est de : {min_consumption:,.2f} kwh')
        print(f'Le coût total de l\énergie consommée est de : {total_cost:,.2f} €')

    results = {
    "Moyenne consommation (Kwh)": [avg_consumption],
    "Max consommation (Kwh)": [max_consumption],
    "Min consommation (Kwh)": [min_consumption],
    "Coût total (€)": [total_cost]
}

    results_df = pd.DataFrame(results)
    results_file = os.path.join("data", "results.csv")
    results_df.to_csv(results_file, index=False)
    print(f"Les résultats ont été sauvegardés dans {results_file}")

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
    plt.xlabel("Date")
    plt.ylabel("Coût (€)")
    plt.title("Coût quotidien de l'énergie consommée")
    plt.xticks(rotation=45)
    plt.legend()
    total_cost_text = f"Coût total : {total_cost:,.2f} €"
    plt.gcf().text(0.15, 0.85, total_cost_text, fontsize=12, color='red', bbox=dict(facecolor='white', alpha=0.8))
    plt.tight_layout()
    plt.show()


    if data.isnull().values.any():
        print("Attention : Le fichier contient des valeurs manquantes. Veuillez les corriger.")
        print(data.isnull().sum())
        return



if __name__ == "__main__":
    main()
