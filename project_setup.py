# common_imports.py

# Struktur & Typen
from pathlib import Path
from typing import Dict, List

# Datenverarbeitung
import json
import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from slugify import slugify  # Zum Vereinheitlichen von Strings

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display

# Statistik
from scipy.stats import linregress, f_oneway
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as mc

# Eigene Module und Funktionen
from kj_core.utils.latex_export import (
    generate_latex_table,
    generate_grouped_latex_tables,
    save_latex_table,
    build_data_dict_df
)
from kj_core.utils.labeling import (
    get_label_from_dict,
    get_color_dict
)
from kj_core import (
    CoreConfig,
    PlotManager,
    get_logger
)

# Projekteinstellungen
from project_config import (
    working_directory,
    data_export_directory,
    latex_export_directory,
    filename_clean_dataset,
    filename_clean_data_dict
)



def load_config_and_plot_manager():
    """
    Lädt die Konfiguration und initialisiert den PlotManager.
    """
    logger = get_logger(__name__)
    try:
        config = CoreConfig(working_directory=f"{working_directory}/combined")
        logger.info(f"--- CONFIG geladen --- \n{config}")
    except Exception as e:
        logger.error("Fehler beim Laden der Konfiguration.", exc_info=True)
        raise

    try:
        plot_manager = PlotManager(config)
        logger.info(f"--- PLOT_MANAGER geladen --- \n{plot_manager}")
    except Exception as e:
        logger.error("Fehler beim Initialisieren des PlotManagers.", exc_info=True)
        raise

    return config, plot_manager, logger


def load_data(logger, directory: Path, filename_dataset: str, filename_data_dict: str):
    """
    Lädt den Datensatz und das Daten-Dictionary aus den angegebenen Dateien.
    """
    try:
        dataset_path = directory / filename_dataset
        df = pd.read_feather(dataset_path)
        logger.info(f"Datensatz erfolgreich geladen von: {dataset_path}")
    except Exception as e:
        logger.error(f"Fehler beim Laden des Datensatzes: {e}", exc_info=True)
        raise

    try:
        dict_path = directory / filename_data_dict
        with open(dict_path, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
        logger.info(f"Daten-Dictionary erfolgreich geladen von: {dict_path}")
    except Exception as e:
        logger.error(f"Fehler beim Laden des Daten-Dictionarys: {e}", exc_info=True)
        raise

    return df, data_dict
