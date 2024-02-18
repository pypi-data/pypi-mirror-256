"""FMP ETF Info Model."""

from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.etf_info import (
    EtfInfoData,
    EtfInfoQueryParams,
)
from openbb_fmp.utils.helpers import create_url, get_data_many
from pydantic import Field


class FMPEtfInfoQueryParams(EtfInfoQueryParams):
    """FMP ETF Info Query."""


class FMPEtfInfoData(EtfInfoData):
    """FMP ETF Info Data."""

    asset_class: Optional[str] = Field(
        default=None, description="Asset class of the ETF."
    )
    aum: Optional[float] = Field(default=None, description="Assets under management.")
    avg_volume: Optional[float] = Field(
        default=None, description="Average trading volume of the ETF."
    )
    cusip: Optional[str] = Field(default=None, description="CUSIP of the ETF.")
    domicile: Optional[str] = Field(default=None, description="Domicile of the ETF.")
    etf_company: Optional[str] = Field(default=None, description="Company of the ETF.")
    expense_ratio: Optional[float] = Field(
        default=None, description="Expense ratio of the ETF."
    )
    isin: Optional[str] = Field(default=None, description="ISIN of the ETF.")
    nav: Optional[float] = Field(
        default=None, description="Net asset value of the ETF."
    )
    nav_currency: Optional[str] = Field(
        default=None, description="Currency of the ETF's net asset value."
    )
    website: Optional[str] = Field(default=None, description="Website link of the ETF.")
    holdings_count: Optional[int] = Field(
        adefault=None, description="Number of holdings in the ETF."
    )


class FMPEtfInfoFetcher(
    Fetcher[
        FMPEtfInfoQueryParams,
        List[FMPEtfInfoData],
    ]
):
    """Transform the query, extract and transform the data from the FMP endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> FMPEtfInfoQueryParams:
        """Transform the query."""
        return FMPEtfInfoQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: FMPEtfInfoQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the FMP endpoint."""
        api_key = credentials.get("fmp_api_key") if credentials else ""

        url = create_url(version=4, endpoint="etf-info", api_key=api_key, query=query)

        return await get_data_many(url, **kwargs)

    @staticmethod
    def transform_data(
        query: FMPEtfInfoQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[FMPEtfInfoData]:
        """Return the transformed data."""
        # remove "sectorList" key from data. it's handled by the sectors
        for d in data:
            d.pop("sectorList", None)
        return [FMPEtfInfoData.model_validate(d) for d in data]
