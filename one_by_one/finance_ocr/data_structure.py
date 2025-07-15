from typing import List

import msgspec


class Image(msgspec.Struct):
    identifier: str
    name: str
    width: int
    height: int


class Polygon(msgspec.Struct):
    id: str
    type: int
    text: str
    points: List[List[float]]


class Annotation(msgspec.Struct):
    polygons: List[Polygon]


class FinanceOcrDataset(msgspec.Struct):
    images: List[Image]
    annotations: List[Annotation]
