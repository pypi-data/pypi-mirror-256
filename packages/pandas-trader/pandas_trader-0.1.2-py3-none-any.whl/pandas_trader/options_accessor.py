import numpy as np
import pandas as pd
from scipy.stats import norm


class OptionsDataFrame(pd.DataFrame):
    def __init__(
        self,
        data: pd.DataFrame,
        option_type_column: str = "option_type",
        asset_price_column: str = "close",
        strike_price_column: str = "strike",
        time_to_expiration_column: str = "time_to_expiration",
        risk_free_rate_column: str = "risk_free_rate",
        volatility_column: str = "volatility",
    ):
        self._validate(data)
        self._obj: pd.DataFrame = data
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
    def is_call(
        self,
    ) -> pd.Series:
        data = self._obj.copy()
        return data[self._option_type_column].str.contains("c")

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
        return call_price.where(self.is_call, other=put_price)

    def delta(
        self,
    ) -> pd.Series:
        """Calculate delta price of call/put"""
        delta = norm.cdf(self.d1, 0, 1)
        return delta.where(self.is_call, other=-delta)

    def gamma(
        self,
    ) -> pd.Series:
        """Calculate gamma of call/put"""
        data = self._obj.copy()
        gamma = norm.pdf(self.d1, 0, 1) / (
            data[self._strike_price_column]
            * data[self._volatility_column]
            * np.sqrt(data[self._time_to_expiration_column])
        )
        return gamma

    def vega(
        self,
    ) -> pd.Series:
        """Calculate vega price of call/put"""
        data = self._obj.copy()
        vega = (
            data[self._asset_price_column]
            * norm.pdf(self.d1, 0, 1)
            * np.sqrt(self._time_to_expiration_column)
        )
        return vega

    def theta(
        self,
    ) -> pd.Series:
        """Calculate theta price of call/put"""
        data = self._obj.copy()
        theta = (
            -data[self._asset_price_column]
            * norm.pdf(self.d1, 0, 1)
            * data[self._volatility_column]
            / (2 * np.sqrt(data[self._time_to_expiration_column]))
        )
        theta_part_2 = (
            data[self._risk_free_rate_column]
            * data[self._strike_price_column]
            * np.exp(
                -data[self._risk_free_rate_column]
                * data[self._time_to_expiration_column]
            )
            * norm.cdf(self.d2, 0, 1)
        )
        theta += theta_part_2.where(~self.is_call, other=-theta_part_2)
        return theta

    def rho(
        self,
    ) -> pd.Series:
        """Calculate rho price of call/put"""
        data = self._obj.copy()
        rho = (
            data[self._strike_price_column]
            * data[self._time_to_expiration_column]
            * np.exp(
                -data[self._risk_free_rate_column]
                * data[self._time_to_expiration_column]
            )
            * norm.cdf(self.d2, 0, 1)
        )
        rho_part_2 = norm.cdf(self.d2.where(self.is_call, other=-self.d2), 0, 1)
        rho *= rho_part_2.where(self.is_call, other=-rho_part_2)
        return rho
