"""YFinance Key Executives Model."""

# pylint: disable=unused-argument
import warnings
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.key_executives import (
    KeyExecutivesData,
    KeyExecutivesQueryParams,
)
from openbb_core.provider.utils.descriptions import QUERY_DESCRIPTIONS
from pydantic import Field
from yfinance import Ticker

_warn = warnings.warn


class YFinanceKeyExecutivesQueryParams(KeyExecutivesQueryParams):
    """YFinance Key Executives Query."""


class YFinanceKeyExecutivesData(KeyExecutivesData):
    """YFinance Key Executives Data."""

    __alias_dict__ = {
        "year_born": "yearBorn",
        "fiscal_year": "fiscalYear",
        "pay": "totalPay",
        "exercised_value": "exercisedValue",
        "unexercised_value": "unexercisedValue",
    }

    exercised_value: Optional[int] = Field(
        default=None,
        description="Value of shares exercised.",
    )
    unexercised_value: Optional[int] = Field(
        default=None,
        description="Value of shares not exercised.",
    )


class YFinanceKeyExecutivesFetcher(
    Fetcher[YFinanceKeyExecutivesQueryParams, List[YFinanceKeyExecutivesData]]
):
    """YFinance Key Executives Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> YFinanceKeyExecutivesQueryParams:
        """Transform the query."""
        return YFinanceKeyExecutivesQueryParams(**params)

    @staticmethod
    def extract_data(
        query: YFinanceKeyExecutivesQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Extract the raw data from YFinance."""
        symbols = query.symbol.split(",")
        symbol = symbols[0]
        if len(symbols) > 1:
            _warn(f"{QUERY_DESCRIPTIONS.get('symbol_list_warning', '')} {symbol}")
        try:
            ticker = Ticker(symbol).get_info()
        except Exception as e:
            raise RuntimeError(f"Error getting data for {symbol}: {e}") from e
        if ticker.get("companyOfficers") is None:
            raise ValueError(f"No executive data found for {symbol}")
        officers_data = ticker.get("companyOfficers", [])
        [d.pop("maxAge") for d in officers_data]  # pylint: disable=W0106
        return officers_data

    @staticmethod
    def transform_data(
        query: YFinanceKeyExecutivesQueryParams,
        data: List[Dict],
        **kwargs: Any,
    ) -> List[YFinanceKeyExecutivesData]:
        """Transform the data."""
        return [YFinanceKeyExecutivesData.model_validate(d) for d in data]
