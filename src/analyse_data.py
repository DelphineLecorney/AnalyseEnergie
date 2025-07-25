import pandas as pd

# Charger les données
df = pd.read_csv("data/energy_data.csv")

# Afficher les premières lignes des données
print(df.head())

# Afficher les informations générales sur les données
print(df.info())

# Vérifier les statistiques descriptives
print(df.describe())
