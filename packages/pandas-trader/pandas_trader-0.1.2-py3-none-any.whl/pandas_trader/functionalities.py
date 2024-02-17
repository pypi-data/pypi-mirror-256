import pandas as pd
import yfinance as yf


def deannualize(annual_rate: float, periods: float = 365) -> float:
    return (1 + annual_rate) ** (1 / periods) - 1


def get_risk_free_rate() -> pd.DataFrame:
    # download 3-month us treasury bills rates
    annualized = yf.download("^IRX")["Adj Close"]
    daily = annualized.apply(deannualize)
    return pd.DataFrame({"annualized": annualized, "daily": daily})
