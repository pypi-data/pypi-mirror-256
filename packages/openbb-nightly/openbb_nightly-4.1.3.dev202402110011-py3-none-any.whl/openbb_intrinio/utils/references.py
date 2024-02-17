"""Intrinio References Helpers."""

from typing import Literal, Optional

from openbb_core.provider.abstract.data import Data
from pydantic import Field

SOURCES = Literal[
    "iex",
    "bats",
    "bats_delayed",
    "utp_delayed",
    "cta_a_delayed",
    "cta_b_delayed",
    "intrinio_mx",
    "intrinio_mx_plus",
    "delayed_sip",
]

VENUES = {
    "A": "NYSE MKT LLC",
    "B": "NASDAQ OMX BX, Inc.",
    "C": "National Stock Exchange Inc. (NSX)",
    "D": "FINRA ADF",
    "I": "International Securities Exchange, LLC",
    "J": "Bats EDGA Exchange, INC",
    "K": "Bats EDGX Exchange, Inc.",
    "M": "Chicago Stock Exchange, Inc. (CHX)",
    "N": "New York Stock Exchange LLC",
    "P": "NYSE Arca, Inc.",
    "S": "Consolidated Tape System",
    "T": "NASDAQ (Tape A, B securities)",
    "Q": "NASDAQ (Tape C securities)",
    "V": "The Investors' Exchange, LLC (IEX)",
    "W": "Chicago Broad Options Exchange, Inc. (CBOE)",
    "X": "NASDAQ OMX PSX, Inc. LLC",
    "Y": "Bats BYX Exchange, Inc.",
    "Z": "Bats BZX Exchange, Inc.",
    "u": "Other OTC Markets",
}


class IntrinioCompany(Data):
    """Intrinio Company Data."""

    id: str = Field(description="The Intrinio ID of the Company.")
    ticker: Optional[str] = Field(
        description="The stock market ticker symbol associated with the company's common stock securities",
        default=None,
    )
    name: Optional[str] = Field(description="The company's common name.", default=None)
    lei: Optional[str] = Field(
        description="The Legal Entity Identifier (LEI) of the company.", default=None
    )
    cik: Optional[str] = Field(
        description="The Central Index Key (CIK) of the company.",
    )


class IntrinioSecurity(Data):
    """Intrinio Security Data."""

    id: str = Field(description="The Intrinio ID for Security.")
    company_id: Optional[str] = Field(
        description="The Intrinio ID for the company for which the Security is issued.",
        default=None,
    )
    name: Optional[str] = Field(description="Name of the Security.", default=None)
    code: Optional[str] = Field(
        description="""
            A 2-3 digit code classifying the Security.
            Reference: https://docs.intrinio.com/documentation/security_codes
        """,
        default=None,
    )
    currency: Optional[str] = Field(
        description="The currency in which the Security is traded.", default=None
    )
    ticker: Optional[str] = Field(
        description="The common/local ticker of the Security.", default=None
    )
    composite_ticker: Optional[str] = Field(
        description="The country-composite ticker of the Security.", default=None
    )
    figi: Optional[str] = Field(description="The OpenFIGI identifier.", default=None)
    composite_figi: Optional[str] = Field(
        description="The country-composite OpenFIGI identifier.", default=None
    )
    share_class_figi: Optional[str] = Field(
        description="The global-composite OpenFIGI identifier.", default=None
    )
    primary_listing: Optional[bool] = Field(
        description="""
            If true, the Security is the primary issue for the company,
            otherwise it is a secondary issue on a secondary stock exchange,
        """,
        default=None,
    )
