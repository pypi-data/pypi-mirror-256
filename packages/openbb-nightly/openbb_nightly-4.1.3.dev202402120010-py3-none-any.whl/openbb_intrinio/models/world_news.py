"""Intrinio World News Model."""

from datetime import datetime
from typing import Any, Dict, List, Optional

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.world_news import (
    WorldNewsData,
    WorldNewsQueryParams,
)
from openbb_core.provider.utils.helpers import filter_by_dates
from openbb_intrinio.utils.helpers import get_data_many
from pydantic import Field, field_validator


class IntrinioWorldNewsQueryParams(WorldNewsQueryParams):
    """Intrinio World News Query.

    Source: https://docs.intrinio.com/documentation/web_api/get_all_company_news_v2
    """


class IntrinioWorldNewsData(WorldNewsData):
    """Intrinio World News Data."""

    __alias_dict__ = {"date": "publication_date", "text": "summary"}

    id: str = Field(description="Article ID.")
    company: Dict[str, Any] = Field(
        description="Company details related to the news article."
    )

    @field_validator("publication_date", mode="before", check_fields=False)
    def date_validate(cls, v):  # pylint: disable=E0213
        """Return the date as a datetime object."""
        return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.000Z")


class IntrinioWorldNewsFetcher(
    Fetcher[
        IntrinioWorldNewsQueryParams,
        List[IntrinioWorldNewsData],
    ]
):
    """Transform the query, extract and transform the data from the Intrinio endpoints."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> IntrinioWorldNewsQueryParams:
        """Transform the query params."""
        return IntrinioWorldNewsQueryParams(**params)

    @staticmethod
    async def aextract_data(
        query: IntrinioWorldNewsQueryParams,
        credentials: Optional[Dict[str, str]],
        **kwargs: Any,
    ) -> List[Dict]:
        """Return the raw data from the Intrinio endpoint."""
        api_key = credentials.get("intrinio_api_key") if credentials else ""

        base_url = "https://api-v2.intrinio.com"
        url = f"{base_url}/companies/news?page_size={query.limit}&api_key={api_key}"

        return await get_data_many(url, "news", **kwargs)

    # pylint: disable=unused-argument
    @staticmethod
    def transform_data(
        query: IntrinioWorldNewsQueryParams, data: List[Dict], **kwargs: Any
    ) -> List[IntrinioWorldNewsData]:
        """Return the transformed data."""
        modeled_data = [IntrinioWorldNewsData.model_validate(d) for d in data]
        return filter_by_dates(modeled_data, query.start_date, query.end_date)
