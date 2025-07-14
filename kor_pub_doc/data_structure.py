from typing import List

import msgspec


class Image(msgspec.Struct):
    file_name: str = msgspec.field(name="image.file.name")
    width: int = msgspec.field(name="image.width")
    height: int = msgspec.field(name="image.height")


class Annotation(msgspec.Struct):
    id: int
    text: str = msgspec.field(name="annotation.text")
    bbox: List[int] = msgspec.field(name="annotation.bbox")


class KorPubDataset(msgspec.Struct):
    images: List[Image]
    annotations: List[Annotation]
