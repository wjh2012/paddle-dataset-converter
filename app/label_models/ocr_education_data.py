from typing import List

import msgspec


class Image(msgspec.Struct):
    identifier: str
    width: int
    height: int


class Bbox(msgspec.Struct):
    data: str
    id: int
    x: List[int]
    y: List[int]


class OcrDataEducationData(msgspec.Struct):
    images: Image = msgspec.field(name="Images")
    bbox: List[Bbox] = msgspec.field(name="Bbox")
