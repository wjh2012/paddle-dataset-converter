from typing import List

import msgspec


class Info(msgspec.Struct):
    name: str
    date_created: str


class Images(msgspec.Struct):
    id: str
    width: int
    height: int
    file_name: str


class Attributes(msgspec.Struct):
    type: str
    # gender: str
    # age: str
    # job: str


class Annotation(msgspec.Struct):
    id: str
    image_id: str
    text: str
    attributes: Attributes
    # bbox: List[object]


class Licenses(msgspec.Struct):
    name: str
    url: str


class KorFontDataset(msgspec.Struct):
    # info: Info
    images: List[Images]
    annotations: List[Annotation]
    # licenses: List[Licenses]


def filter_annotations(data: KorFontDataset) -> List[Annotation]:
    return [ann for ann in data.annotations if ann.attributes.type == "단어(어절)"]
