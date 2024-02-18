"""SSE DTOs"""

from typing import Literal, Union

from ..compat import Sequence, TypedDict
from .calculation import MetisCalculationDTO
from .collection import MetisCollectionDTO, MetisCollectionTypeDTO
from .datasource import MetisDataSourceDTO
from .error import MetisErrorDTO

MetisEventType = Literal["calculations", "collections", "datasources", "errors", "pong"]


class MetisErrorEventDataDTO(TypedDict):
    "Errors event data DTO"
    req_id: str
    data: Sequence[MetisErrorDTO]


class MetisErrorEventDTO(TypedDict):
    "Errors event DTO"
    type: Literal["errors"]
    data: MetisErrorEventDataDTO


class MetisPongEventDTO(TypedDict):
    "Pong event DTO"
    type: Literal["pong"]
    data: None


class MetisDataSourcesEventDataDTO(TypedDict):
    "Data sources event data DTO"
    req_id: str
    data: Sequence[MetisDataSourceDTO]
    total: int
    types: Sequence[MetisCollectionTypeDTO]


class MetisDataSourcesEventDTO(TypedDict):
    "Data sources event DTO"
    type: Literal["datasources"]
    data: MetisDataSourcesEventDataDTO


class MetisCalculationsEventDataDTO(TypedDict):
    "Calculations event data DTO"
    req_id: str
    data: Sequence[MetisCalculationDTO]
    total: int
    types: Sequence[MetisCollectionTypeDTO]


class MetisCalculationsEventDTO(TypedDict):
    "Calculations event DTO"
    type: Literal["calculations"]
    data: MetisCalculationsEventDataDTO


class MetisCollectionsEventDataDTO(TypedDict):
    "Collections event data DTO"
    req_id: str
    data: Sequence[MetisCollectionDTO]
    total: int
    types: Sequence[MetisCollectionTypeDTO]


class MetisCollectionsEventDTO(TypedDict):
    "Collections event DTO"
    type: Literal["collections"]
    data: MetisCollectionsEventDataDTO


# pylint: disable=invalid-name
MetisEventDTO = Union[
    MetisCalculationsEventDTO,
    MetisCollectionsEventDTO,
    MetisDataSourcesEventDTO,
    MetisErrorEventDTO,
    MetisPongEventDTO,
]
