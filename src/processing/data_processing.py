import os
import pandas as pd

def load_data(data_file):
    if not os.path.exists(data_file):
        print(f"Aucun fichier de données trouvé : {data_file}")
        return None

    data = pd.read_csv(data_file)
    required_columns = {"date", "index", "price_per_kwh", "devices", "temps"}
    if not required_columns.issubset(data.columns):
        raise ValueError(f"Les colonnes nécessaires sont : {required_columns}")

    data["date"] = pd.to_datetime(data["date"])
    data["consumption_kwh"] = data["index"].diff().fillna(0)
    data["cost"] = data["consumption_kwh"] * data["price_per_kwh"]
    return data
