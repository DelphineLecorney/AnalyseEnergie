import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import matplotlib.dates as mdates
import os


def plot_data(data):

    # Couleurs associées à chaque type de météo
    weather_colors = {
        "pluie": "gray",
        "soleil": "mediumaquamarine",
        "mitigé": "darkgray",
        "gris": "dimgray"
    }

    # Ajout d'une colonne 'color' en fonction de la météo
    data["color"] = data["temps"].map(weather_colors)

    # Création de la figure avec un axe principal (consommation)
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Affichage des barres de consommation
    bars = ax1.bar(
        data["date"],
        data["consumption_kwh"],
        color=data["color"],
        width=0.7,
        label="Consommation (kWh)"
    )

    # Ligne de consommation moyenne
    avg = data["consumption_kwh"].mean()
    ax1.axhline(avg, color="darkslategray", linestyle=":", linewidth=2, label="Moyenne Conso")


    ax1.set_ylabel("Consommation (kWh)", color="black")
    ax1.tick_params(axis="y", labelcolor="black")

    # Deuxième axe Y pour le coût (€)
    ax2 = ax1.twinx()
    ax2.plot(data["date"], data["cost"], marker="o", color="teal", label="Coût quotidien (€)")
    ax2.set_ylabel("Coût (€)", color="teal")
    ax2.tick_params(axis="y", labelcolor="teal")

    # Format de la date sur l’axe X
    ax1.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
    ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
    fig.autofmt_xdate(rotation=45)


    # Création des légendes météo + séries
    weather_legend = [plt.Line2D([0], [0], color=color, lw=4) for color in weather_colors.values()]
    weather_labels = [weather.capitalize() for weather in weather_colors.keys()]
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()

    # Affichage de la légende complète
    plt.title("Consommation énergétique quotidienne avec conditions météorologiques")
    plt.legend(
        weather_legend + handles1 + handles2,
        weather_labels + labels1 + labels2,
        loc="upper left",
        ncol=1
    )

    # Enregistrement automatique du graphique
    current_dir = os.getcwd()
    while not any(folder in os.listdir(current_dir) for folder in ['data', 'src']):
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            break
        current_dir = parent_dir

    images_dir = os.path.join(current_dir, "images")
    #os.makedirs(images_dir, exist_ok=True)

    plt.savefig(os.path.join(images_dir, "plot_static.png"), dpi=300)
    plt.tight_layout()
    plt.show()  # Fenêtre interactive à fermer manuellement



"""Affichage interactif avec Plotly dans le navigateur."""

def plot_data_interactive(data):
    
    # Couleurs météo
    weather_colors = {
        "pluie": "gray",
        "soleil": "mediumaquamarine",
        "mitigé": "darkgray",
        "gris": "dimgray"
    }
    data["color"] = data["temps"].map(weather_colors)
    avg_consumption = data["consumption_kwh"].mean()

    # Création d'une figure Plotly
    fig = go.Figure()

    weather_types = list(weather_colors.keys())
    bar_traces = []

    # Barres de consommation pour chaque météo
    for weather in weather_types:
        filtered = data[data["temps"] == weather]
        custom_filtered = np.stack((filtered["temps"], filtered["devices"]), axis=-1)

        trace = go.Bar(
            x=filtered["date"],
            y=filtered["consumption_kwh"],
            name=f"Conso ({weather})",
            marker_color=weather_colors[weather],
            customdata=custom_filtered,
            hovertemplate='<b>Date:</b> %{x}<br>' +
                          '<b>Conso:</b> %{y} kWh<br>' +
                          '<b>Météo:</b> %{customdata[0]}<br>' +
                          '<b>Appareils:</b><br>%{customdata[1]}<extra></extra>',
            yaxis='y1',
            visible=True
        )

        fig.add_trace(trace)
        bar_traces.append(trace)


    # Ajout de la courbe des coûts
    fig.add_trace(go.Scatter(
        x=data["date"],
        y=data["cost"],
        name="Coût (€)",
        mode="lines+markers",
        marker=dict(color="teal"),
        yaxis='y2',
        hovertemplate='<b>Date:</b> %{x}<br>' +
                      '<b>Coût:</b> %{y:.2f} €<extra></extra>',
        visible=True
    ))
    
    
    # Ligne de moyenne de consommation 
    fig.add_trace(go.Scatter(
        x=data["date"],
        y=[avg_consumption] * len(data),
        mode="lines",
        name="Moyenne Conso",
        line=dict(color="darkslategray", dash="dot"),
        hoverinfo="skip",
        yaxis='y1',
        visible=True
    ))

    # Menu déroulant
    buttons = []

    # Bouton "Toutes"
    visible_all = [True] * len(bar_traces) + [True, True]
    buttons.append(dict(
        label="Toutes",
        method="update",
        args=[{"visible": visible_all}]
    ))

    # Boutons par météo
    for i, weather in enumerate(weather_types):
        visible = [False] * len(bar_traces)
        visible[i] = True
        visible += [True, True]  # coût + moyenne
        buttons.append(dict(
            label=weather.capitalize(),
            method="update",
            args=[{"visible": visible}]
        ))

    # Mise en page avec axes doubles
    fig.update_layout(
        title="Consommation énergétique quotidienne (interactif)",
        xaxis=dict(
            title="Date",
            tickangle=45,
            tickfont=dict(size=10),
        ),
        yaxis=dict(title="Consommation (kWh)", side="left"),
        yaxis2=dict(
            title="Coût (€)",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(x=0.01, y=1.15, orientation="h"),
        hovermode="x unified",
        template="plotly_white"
    )

    # Forcer ouverture dans le navigateur par défaut
    pio.renderers.default = 'browser'
    fig.show()
