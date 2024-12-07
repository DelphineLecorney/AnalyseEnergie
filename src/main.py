# src/main.py
import os
from generate_data import generate_data
from analyse_data import analyse_data

def main():
    # Étape 1 : Générer les données si elles n'existent pas déjà
    data_file = 'data/energie_data.csv'
    if not os.path.exists(data_file):
        print("Génération des données...")
        generate_data(data_file)
    
    # Étape 2 : Analyser les données
    print("Analyse des données...")
    analyse_data(data_file)

if __name__ == "__main__":
    main()
