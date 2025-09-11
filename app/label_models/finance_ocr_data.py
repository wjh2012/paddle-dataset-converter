from typing import List

import msgspec


class Image(msgspec.Struct):
    # identifier: str
    name: str
    # width: int
    # height: int


class Bbox(msgspec.Struct):
    id: str
    x: float
    y: float
    width: float
    height: float


class Polygon(msgspec.Struct):
    # id: str
    # type: int
    text: str
    points: List[List[float]]


class Annotation(msgspec.Struct):
    polygons: List[Polygon]
    # bbox: List[Bbox]


class FinanceOcrData(msgspec.Struct):
    images: List[Image]
    annotations: List[Annotation]
