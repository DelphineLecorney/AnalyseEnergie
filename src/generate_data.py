import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_energy_data(start_date="2024-12-06", days=45, output_file="data/energy_data.csv"):
    devices_list = [
        "Fridge", "Oven", "TV", "Dryer", "PC", "Dishwasher", "Heater", 
        "Washer", "Microwave", "AC", "Toaster", "Coffee Machine", "Lamp", "Router"
    ]
    weather_options = ["soleil", "pluie", "mitigé", "gris"]

    data = []
    index = 8000
    current_date = datetime.strptime(start_date, "%Y-%m-%d")

    for _ in range(days):
        # Probabilité de production (ex: panneaux → index peut baisser)
        solar_production = random.random() < 0.15  # 15% de chances de production nette

        daily_devices = random.sample(devices_list, k=random.randint(1, 6))
        daily_weather = random.choice(weather_options)
        price_per_kwh = round(random.uniform(0.09, 0.15), 2)

        if solar_production and daily_weather == "soleil":
            consumption = -random.randint(100, 300)  # injection : index diminue
        else:
            consumption = random.randint(50, 200)  # consommation classique

        new_index = max(0, index + consumption)  # éviter index négatif
        data.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "index": new_index,
            "price_per_kwh": price_per_kwh,
            "devices": ", ".join(daily_devices),
            "temps": daily_weather
        })

        index = new_index
        current_date += timedelta(days=1)

    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"✅ Données générées avec injection solaire possible, sauvegardées dans : {output_file}")

if __name__ == "__main__":
    generate_energy_data()
