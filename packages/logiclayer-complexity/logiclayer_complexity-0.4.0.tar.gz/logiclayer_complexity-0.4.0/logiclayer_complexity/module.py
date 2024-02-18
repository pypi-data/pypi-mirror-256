"""Economic Complexity adapter for use in LogicLayer.

Contains a module to enable endpoints which return economic complexity
calculations, using a Tesseract OLAP server as data source.
"""

import asyncio
from typing import Dict, List, Optional, Tuple

import pandas as pd
from fastapi import Depends, Header, HTTPException, Request
from fastapi.responses import RedirectResponse
from logiclayer import LogicLayerModule, route
from tesseract_olap import DataRequest, OlapServer
from tesseract_olap.backend.exceptions import BackendError
from tesseract_olap.query.exceptions import QueryError
from typing_extensions import Annotated

from .__version__ import __title__, __version__
from .common import ResponseFormat
from .complexity import (
    ComplexityParameters,
    ComplexitySubnationalParameters,
    prepare_complexity_params,
    prepare_complexity_subnational_params,
)
from .dependencies import parse_alias, parse_filter
from .opportunity_gain import OpportunityGainParameters, prepare_opportunity_gain_params
from .peii import PEIIParameters, prepare_peii_params
from .pgi import PGIParameters, prepare_pgi_params
from .rca import (
    RcaParameters,
    RcaSubnationalParameters,
    prepare_rca_params,
    prepare_subnatrca_params,
)
from .relatedness import (
    RelatednessParameters,
    RelatednessSubnationalParameters,
    prepare_relatedness_params,
    prepare_relatedness_subnational_params,
)
from .wdi import WdiParameters, WdiReference, WdiReferenceSchema, parse_wdi


class EconomicComplexityModule(LogicLayerModule):
    """Economic Complexity calculations module class for LogicLayer."""

    server: "OlapServer"
    wdi: Optional["WdiReference"]

    def __init__(
        self,
        server: "OlapServer",
        wdi: Optional["WdiReferenceSchema"] = None,
    ):
        """Setups the server for this instance."""
        super().__init__()

        if server is None:
            raise ValueError(
                "EconomicComplexityModule requires a tesseract_olap.OlapServer instance"
            )

        self.server = server
        self.wdi = None if wdi is None else WdiReference(**wdi)

    async def fetch_data(self, query: DataRequest):
        """Retrieves the data from the backend, and handles related errors."""
        try:
            res = await self.server.execute(query)
        except QueryError as exc:
            raise HTTPException(status_code=400, detail=exc.message) from None
        except BackendError as exc:
            raise HTTPException(status_code=500, detail=exc.message) from None

        return pd.DataFrame([item async for item in res])

    async def apply_wdi_threshold(
        self,
        df: pd.DataFrame,
        wdi_params: WdiParameters,
        location: str,
    ):
        if self.wdi is None:
            raise HTTPException(500, "WDI reference is not configured")

        wdi_location = self.wdi.level_mapper.get(location, location)
        wdi_query = self.wdi.build_query(wdi_params, wdi_location)
        wdi_data = await self.fetch_data(wdi_query)
        wdi_members = wdi_data[f"{wdi_location} ID"].to_list()

        # WDI works the same as threshold, but using remote data
        data_to_drop = df.loc[~df[f"{location} ID"].isin(wdi_members)]
        df.drop(data_to_drop.index, inplace=True)

        del wdi_data, data_to_drop

    @route("GET", "/")
    def route_root(self):
        return {
            "module": __title__,
            "version": __version__,
            "wdi": "disabled" if self.wdi is None else "enabled",
        }

    @route("GET", "/rca.{extension}")
    async def route_rca(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: RcaParameters = Depends(prepare_rca_params),
        wdi: List[WdiParameters] = Depends(parse_wdi),
    ):
        """RCA calculation endpoint."""
        df = await self.fetch_data(params.request)

        params.apply_threshold(df)
        for item in wdi:
            await self.apply_wdi_threshold(df, item, params.location)

        df_rca = params.calculate(df)

        apply_filters(df_rca, filters)
        apply_aliases(df_rca, aliases)

        return extension.serialize(df_rca)

    @route("GET", "/eci.{extension}")
    async def route_eci(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: ComplexityParameters = Depends(prepare_complexity_params),
        wdi: List[WdiParameters] = Depends(parse_wdi),
    ):
        """ECI calculation endpoint."""
        df = await self.fetch_data(params.request)

        params.rca_params.apply_threshold(df)
        for item in wdi:
            await self.apply_wdi_threshold(df, item, params.rca_params.location)

        df_eci = params.calculate(df, "ECI")

        apply_filters(df_eci, filters)
        apply_aliases(df_eci, aliases)

        return extension.serialize(df_eci)

    @route("GET", "/pci.{extension}")
    async def route_pci(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: ComplexityParameters = Depends(prepare_complexity_params),
        wdi: List[WdiParameters] = Depends(parse_wdi),
    ):
        """PCI calculation endpoint."""
        df = await self.fetch_data(params.request)

        params.rca_params.apply_threshold(df)
        for item in wdi:
            await self.apply_wdi_threshold(df, item, params.rca_params.location)

        df_pci = params.calculate(df, "PCI")

        apply_filters(df_pci, filters)
        apply_aliases(df_pci, aliases)

        return extension.serialize(df_pci)

    @route("GET", "/relatedness.{extension}")
    async def route_relatedness(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: RelatednessParameters = Depends(prepare_relatedness_params),
    ):
        """Relatedness calculation endpoint."""
        df = await self.fetch_data(params.request)

        params.rca_params.apply_threshold(df)

        df_reltd = params.calculate(df)

        apply_filters(df_reltd, filters)
        apply_aliases(df_reltd, aliases)

        return extension.serialize(df_reltd)

    @route("GET", "/opportunity_gain.{extension}")
    async def route_opportunity_gain(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: OpportunityGainParameters = Depends(prepare_opportunity_gain_params),
    ):
        """Opportunity Gain calculation endpoint."""
        df = await self.fetch_data(params.request)

        params.rca_params.apply_threshold(df)

        df_opgain = params.calculate(df)

        apply_filters(df_opgain, filters)
        apply_aliases(df_opgain, aliases)

        return extension.serialize(df_opgain)

    @route("GET", "/pgi.{extension}")
    async def route_pgi(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: PGIParameters = Depends(prepare_pgi_params),
    ):
        """PGI calculation endpoint."""
        df, df_gini = await asyncio.gather(
            self.fetch_data(params.rca_params.request),
            self.fetch_data(params.request),
        )

        params.rca_params.apply_threshold(df)

        df_pgi = params.calculate(df, df_gini)

        apply_filters(df_pgi, filters)
        apply_aliases(df_pgi, aliases)

        return extension.serialize(df_pgi)

    @route("GET", "/peii.{extension}")
    async def route_peii(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: PEIIParameters = Depends(prepare_peii_params),
    ):
        """PEII calculation endpoint."""
        df, df_emissions = await asyncio.gather(
            self.fetch_data(params.rca_params.request),
            self.fetch_data(params.request),
        )

        params.rca_params.apply_threshold(df)

        df_peii = params.calculate(df, df_emissions)

        apply_filters(df_peii, filters)
        apply_aliases(df_peii, aliases)

        return extension.serialize(df_peii)

    @route("GET", "/rca_subnational.{extension}")
    async def route_rca_subnational(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: RcaSubnationalParameters = Depends(prepare_subnatrca_params),
    ):
        df_subnat, df_global = await asyncio.gather(
            self.fetch_data(params.subnat_params.request),
            self.fetch_data(params.global_params.request),
        )

        df_rca = params.calculate(df_subnat, df_global)

        apply_filters(df_rca, filters)
        apply_aliases(df_rca, aliases)

        return extension.serialize(df_rca)

    @route("GET", "/eci_subnational.{extension}")
    async def route_eci_subnational(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: ComplexitySubnationalParameters = Depends(
            prepare_complexity_subnational_params
        ),
    ):
        """ECI calculation endpoint."""
        df_subnat, df_global = await asyncio.gather(
            self.fetch_data(params.rca_params.subnat_params.request),
            self.fetch_data(params.rca_params.global_params.request),
        )

        df_eci = params.calculate(df_subnat, df_global, "ECI")

        apply_filters(df_eci, filters)
        apply_aliases(df_eci, aliases)

        return extension.serialize(df_eci)

    @route("GET", "/pci_subnational.{extension}")
    async def route_pci_subnational(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: ComplexitySubnationalParameters = Depends(
            prepare_complexity_subnational_params
        ),
    ):
        """PCI calculation endpoint."""
        df_subnat, df_global = await asyncio.gather(
            self.fetch_data(params.rca_params.subnat_params.request),
            self.fetch_data(params.rca_params.global_params.request),
        )

        df_pci = params.calculate(df_subnat, df_global, "PCI")

        apply_filters(df_pci, filters)
        apply_aliases(df_pci, aliases)

        return extension.serialize(df_pci)

    @route("GET", "/relatedness_subnational.{extension}")
    async def route_relatedness_subnational(
        self,
        extension: ResponseFormat,
        aliases: Dict[str, str] = Depends(parse_alias),
        filters: Dict[str, Tuple[str, ...]] = Depends(parse_filter),
        params: RelatednessSubnationalParameters = Depends(
            prepare_relatedness_subnational_params
        ),
    ):
        """Relatedness calculation endpoint."""
        df_subnat, df_global = await asyncio.gather(
            self.fetch_data(params.rca_params.subnat_params.request),
            self.fetch_data(params.rca_params.global_params.request),
        )

        df_reltd = params.calculate(df_subnat, df_global)

        apply_filters(df_reltd, filters)
        apply_aliases(df_reltd, aliases)

        return extension.serialize(df_reltd)

    @route("GET", "/{endpoint}", response_class=RedirectResponse)
    def route_redirect(
        self,
        request: Request,
        endpoint: str,
        accept: Annotated[Optional[str], Header()] = None,
    ):
        # TODO: check the endpoint exists; requires update in LogicLayerModule
        if accept is None or accept.startswith("*/*") or "text/csv" in accept:
            fmt = ResponseFormat.csv
        elif "application/x-jsonarray" in accept:
            fmt = ResponseFormat.jsonarrays
        elif "application/x-jsonrecords" in accept:
            fmt = ResponseFormat.jsonrecords
        elif "text/tab-separated-values" in accept:
            fmt = ResponseFormat.tsv
        else:
            raise ValueError(
                f"Requested invalid format: '{accept}'. "
                "Prefer an explicit format using a path with a filetype extension."
            )

        url = request.url
        path, endpoint = url.path.rsplit("/", maxsplit=1)
        return f"{path}/{endpoint}.{fmt}?{url.query}"


def apply_filters(df: pd.DataFrame, filters: Dict[str, Tuple[str, ...]]):
    # filter which members will be sent in the response
    for key, values in filters.items():
        column_id = f"{key} ID"
        dropping = df.loc[~df[column_id].isin(values)].index
        df.drop(dropping, inplace=True)
        del dropping


def apply_aliases(df: pd.DataFrame, aliases: Dict[str, str]):
    df.rename(columns=aliases, inplace=True)
