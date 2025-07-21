from src.data_models import InputTransactions
from pathlib import Path
import pandas as pd
from typing import Optional
import httpx


def load_data(filepath: Path):
    """
    Load JSON data from a file and validate it against InputTransactions schema.

    Args:
        filepath (Path): Path to the JSON file to load

    Returns:
        pandas.DataFrame: The loaded and validated transaction data

    Raises:
        Exception: If data validation fails, prints error message but continues
    """
    with filepath.open("+r", encoding="utf-8") as f:
        data = pd.read_json(f)
    try:
        InputTransactions.validate(data)
    except Exception as e:
        print(f"Error raised during dataframe validation {e}")
    return data


def download_pdf(web_url: Optional[str] = None):
    """
    Download a PDF file from a web URL and save it to the local data directory.

    Args:
        web_url (Optional[str]): The URL of the PDF to download. If None or empty,
                               defaults to a wealth-building book PDF.

    Returns:
        None

    Raises:
        None: Errors are handled internally and printed to console.

    Note:
        The PDF is saved as 'build-wealth.pdf' in the data directory relative to this file.
        If the download fails, an error message is printed but no exception is raised.
    """
    if web_url is None:
        web_url = "http://csinvesting.org/wp-content/uploads/2013/07/Little-Book-That-Builds-Wealth_Dorsey.pdf"
    with httpx.Client() as client:
        response = client.get(web_url)

        if response.status_code == 200:
            pdf_filepath = Path(__file__).parents[1] / "data" / "build-wealth.pdf"
            with pdf_filepath.open(mode="wb") as file:
                file.write(response.content)
        else:
            print(f"Failed to download {response.status_code}")
