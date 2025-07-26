import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np


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
    plt.tight_layout()
    plt.show()  # Fenêtre interactive à fermer manuellement

def plot_data_interactive(data):
    """Affichage interactif avec Plotly dans le navigateur."""

    # Couleurs météo
    weather_colors = {
        "pluie": "gray",
        "soleil": "mediumaquamarine",
        "mitigé": "darkgray",
        "gris": "dimgray"
    }
    data["color"] = data["temps"].map(weather_colors)
    customdata = np.stack((data["temps"], data["devices"]), axis=-1)


    # Création d'une figure Plotly
    fig = go.Figure()

    avg_consumption = data["consumption_kwh"].mean()

    fig.add_trace(go.Bar(
    x=data["date"],
    y=data["consumption_kwh"],
    name="Consommation (kWh)",
    marker_color=data["color"],
    customdata=customdata,
    hovertemplate='<b>Date:</b> %{x}<br>' +
                  '<b>Conso:</b> %{y} kWh<br>' +
                  '<b>Météo:</b> %{customdata[0]}<br>' +
                  '<b>Appareils:</b><br>%{customdata[1]}<extra></extra>',
    yaxis='y1'
))


    # Ajout de la courbe des coûts
    fig.add_trace(go.Scatter(
        x=data["date"],
        y=data["cost"],
        name="Coût (€)",
        mode="lines+markers",
        marker=dict(color="teal"),
        yaxis='y2',
        hovertemplate='<b>Date:</b> %{x}<br>' +
                      '<b>Coût:</b> %{y:.2f} €<extra></extra>'
    ))
    
    
    # 4. Ligne de moyenne de consommation 
    fig.add_trace(go.Scatter(
        x=data["date"],
        y=[avg_consumption] * len(data),
        mode="lines",
        name="Moyenne Conso",
        line=dict(color="darkslategray", dash="dot"),
        hoverinfo="skip",
        yaxis='y1'
    ))


    # Mise en page avec axes doubles
    fig.update_layout(
        title="Consommation énergétique quotidienne (interactif)",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Consommation (kWh)", side="left"),
        yaxis2=dict(
            title="Coût (€)",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(x=0.01, y=1.15, orientation="h"),
        hovermode="x unified",  # Affiche toutes les infos en un seul encart
        template="plotly_white"
    )

    # Forcer ouverture dans le navigateur par défaut
    pio.renderers.default = 'browser'
    fig.show()
