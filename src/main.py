import argparse
from processing.data_processing import load_data
from processing.statistics_ import save_statistics
from visualization.visualization import plot_data, plot_data_interactive

def main():
    # Création du parser d'arguments pour la ligne de commande
    parser = argparse.ArgumentParser(description="Analyse énergétique quotidienne")
    parser.add_argument('--file', type=str, default="data/energy_data.csv", help="Chemin vers le fichier CSV")
    parser.add_argument('--save-stats', action='store_true', help="Sauvegarder les statistiques en JSON")
    parser.add_argument('--show-plot', action='store_true', help="Afficher un graphique")
    parser.add_argument('--interactive', action='store_true', help="Utiliser le graphique interactif Plotly")
    args = parser.parse_args()

    print("Chargement des données...")
    data = load_data(args.file)
    if data is None:
        return

    if args.save_stats:
        save_statistics(data)

    if args.show_plot:
        if args.interactive:
            plot_data_interactive(data)
        else:
            plot_data(data)

if __name__ == "__main__":
    main()
