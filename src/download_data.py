# download_data.py

import yfinance as yf
import pandas as pd


def download_price_data(
    ticker: str,
    start_date: str,
    end_date: str = None
) -> pd.DataFrame:

    data = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )

    return data


def save_to_csv(
    data: pd.DataFrame,
    filepath: str
):

    data.to_csv(filepath)

    print(f"Saved to {filepath}")