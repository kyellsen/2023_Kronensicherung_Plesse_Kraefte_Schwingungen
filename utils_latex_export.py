from pathlib import Path
from slugify import slugify
import pandas as pd


def create_caption(caption: str, caption_long: str = None) -> str:
    """
    Create a LaTeX caption string using short and optional long form.

    Parameters:
        caption (str): The short caption for the table.
        caption_long (str, optional): The long caption for the table. Defaults to None.

    Returns:
        str: The LaTeX caption string.
    """
    if caption_long:
        return f"\\caption[{caption}]{{{caption_long}}}"
    return f"\\caption{{{caption}}}"


def create_label(caption: str, additional_label: str = None) -> str:
    """
    Create a LaTeX label string, optionally extended with an additional label.

    Parameters:
        caption (str): The short caption for the table.
        additional_label (str, optional): Additional text to append to the label. Defaults to None.

    Returns:
        str: The LaTeX label string.
    """
    label_clean = slugify(caption, separator="_")
    if additional_label:
        additional_label_clean = slugify(additional_label, separator="_")
        return f"{label_clean}_{additional_label_clean}"
    return label_clean


def generate_latex_table(latex_string: str, caption_text: str, label_clean: str) -> str:
    """
    Generate a LaTeX table string with the provided content, captions, and label.

    Parameters:
        latex_string (str): The LaTeX string of the table.
        caption_text (str): The LaTeX caption string.
        label_clean (str): The LaTeX label string.

    Returns:
        str: The complete LaTeX table string.
    """
    return f"""
    \\begin{{table}}[h]
        \\centering
        {caption_text}
        \\begin{{adjustbox}}{{max width=\\linewidth, max height=\\textheight}}
        {latex_string}
        \\end{{adjustbox}}
        \\label{{tab:{label_clean}}}
    \\end{{table}}
    """


def save_to_file(content: str, file_path: Path) -> None:
    """
    Save the given content to a specified file.

    Parameters:
        content (str): The content to save.
        file_path (Path): The file path where the content should be saved.

    Returns:
        None
    """
    file_path.write_text(content.strip(), encoding="utf-8")
    print(f"Content saved to: {file_path}")


def save_latex_table(latex_string: str, caption: str, latex_export_directory: Path, caption_long: str = None,
                     additional_label: str = None) -> None:
    """
    Save a LaTeX table to the specified directory.

    Parameters:
        latex_string (str): The LaTeX string of the table.
        caption (str): The short caption for the table.
        latex_export_directory (Path): Path object for the export directory.
        caption_long (str, optional): The long caption for the table. Defaults to None.
        additional_label (str, optional): Additional text to append to the label. Defaults to None.

    Returns:
        None
    """
    try:
        label_clean = create_label(caption, additional_label)
        caption_text = create_caption(caption, caption_long)
        latex_table = generate_latex_table(latex_string, caption_text, label_clean)
        latex_path = latex_export_directory / f"{label_clean}.tex"
        save_to_file(latex_table, latex_path)
    except Exception as e:
        print(f"Error saving LaTeX table: {e}")


def extract_latex_dict_from_json(data_dict: dict, keys: list[str], fields: list[str]) -> pd.DataFrame:
    """
    Extrahiere eine LaTeX-kompatible Data-Dictionary-Tabelle aus einem JSON-Daten-Dictionary.

    Escaped nur den "Variable"-Key für LaTeX (z.B. "sensor_id" → "sensor\\_id").

    Parameters:
        data_dict (dict): Vollständiges Daten-Dictionary (z.B. aus JSON geladen)
        keys (list[str]): Liste der auszuwertenden Variablennamen
        fields (list[str]): Liste der Felder (Spalten) für die LaTeX-Tabelle

    Returns:
        pd.DataFrame: DataFrame mit den gewählten Feldern und LaTeX-kompatiblen Inhalten
    """
    result = {field: [] for field in fields}
    for key in keys:
        for field in fields:
            if field == "Variable":
                result["Variable"].append(key.replace("_", "\\_"))
            else:
                result[field].append(data_dict[key][field])
    return pd.DataFrame(result)
