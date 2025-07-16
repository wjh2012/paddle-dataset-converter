from typing import List

import msgspec


class Image(msgspec.Struct):
    identifier: str
    width: int
    height: int


class Bbox(msgspec.Struct):
    data: str
    x: List[int]
    y: List[int]


class OcrDataFinance(msgspec.Struct):
    images: Image = msgspec.field(name="Images")
    bbox: List[Bbox] = msgspec.field(name="bbox")
