# project_config.py
from pathlib import Path

# Hauptpfad des Projekts
main_path = Path(r"C:\kyellsen\005_Projekte\2024_BA\032_Feldversuch_2023_Plesse")

# Analyse-Name
analyse_name = "2023_Kronensicherung_Plesse_Kraefte_Schwingungen"

# Gemeinsame Datenpfade
data_path = main_path / "020_Daten"
working_directory = main_path / "030_Analysen" / analyse_name / "working_directory"
data_export_directory = working_directory / "export_data"
latex_export_directory = working_directory / "export_latex"

filename_clean_dataset = "_dataset_clean.feather"
filename_clean_data_dict = "_data_dict_clean.json"

# Verzeichnisse sicherstellen
data_export_directory.mkdir(parents=True, exist_ok=True)
latex_export_directory.mkdir(parents=True, exist_ok=True)



