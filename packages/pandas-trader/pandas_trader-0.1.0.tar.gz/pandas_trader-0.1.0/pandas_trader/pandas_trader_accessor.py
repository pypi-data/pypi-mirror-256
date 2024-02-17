import numpy as np
import pandas as pd
from scipy.stats import norm


@pd.api.extensions.register_dataframe_accessor("trd")
class OptionsAccessor:
    def __init__(
        self,
        pandas_obj,
        option_type_column: str = "option_type",
        asset_price_column: str = "close",
        strike_price_column: str = "strike",
        time_to_expiration_column: str = "time_to_expiration",
        risk_free_rate_column: str = "risk_free_rate",
        volatility_column: str = "volatility",
    ):
        self._validate(pandas_obj)
        self._obj: pd.DataFrame = pandas_obj
        self._option_type_column = option_type_column
        self._asset_price_column = asset_price_column
        self._strike_price_column = strike_price_column
        self._time_to_expiration_column = time_to_expiration_column
        self._risk_free_rate_column = risk_free_rate_column
        self._volatility_column = volatility_column

    @staticmethod
    def _validate(obj):
        if not isinstance(obj, pd.DataFrame):
            raise AttributeError("Must be `pd.DataFrame`.")

    @property
    def d1(
        self,
    ) -> pd.Series:
        data = self._obj.copy()
        d1 = (
            np.log(data[self._asset_price_column] / data[self.strike_price_column])
            + (data[self.risk_free_rate_column] + data[self.volatility_column] ** 2 / 2)
            * data[self.time_to_expiration_column]
        ) / (
            data[self.volatility_column] * np.sqrt(data[self.time_to_expiration_column])
        )
        return d1

    @property
    def d2(
        self,
    ) -> pd.Series:
        data = self._obj.copy()
        d2 = self.d1 - data[self.volatility_column] * np.sqrt(
            data[self.time_to_expiration_column]
        )
        return d2

    def black_scholes(
        self,
    ) -> pd.Series:
        """Calculate BS price of call/put"""
        data = self._obj.copy()
        call_price = data[self._asset_price_column] * norm.cdf(self.d1, 0, 1) - data[
            self._strike_price_column
        ] * np.exp(
            -data[self._risk_free_rate_column] * data[self._time_to_expiration_column]
        ) * norm.cdf(
            self.d2, 0, 1
        )
        put_price = data[self._strike_price_column] * np.exp(
            -data[self._risk_free_rate_column] * data[self._time_to_expiration_column]
        ) * norm.cdf(-self.d2, 0, 1) - data[self._asset_price_column] * norm.cdf(
            -self.d1, 0, 1
        )
        price = call_price.where(
            data[self._option_type_column].str.contains("c"), other=put_price
        )
        return price

    def delta(
        self,
    ) -> pd.Series:
        """Calculate delta price of call/put"""
        data = self._obj.copy()
        delta = norm.cdf(self.d1, 0, 1)
        delta = delta.where(
            data[self._option_type_column].str.contains("c"), other=-delta
        )
        return delta

    def gamma(
        self,
    ) -> pd.Series:
        """Calculate gamma price of call/put"""
        data = self._obj.copy()
        delta = norm.cdf(self.d1, 0, 1)
        delta = delta.where(
            data[self._option_type_column].str.contains("c"), other=-delta
        )
        return delta
