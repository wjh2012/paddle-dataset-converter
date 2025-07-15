from typing import List

import msgspec


class Info(msgspec.Struct):
    name: str
    date_created: str


class Image(msgspec.Struct):
    file_name: str
    width: int
    height: int


class License(msgspec.Struct):
    output: str
    font: str
    font_no: str
    font_license: str
    font_url: str
    writer_no: str
    writer_gender: str
    writer_age: str


class Word(msgspec.Struct):
    wordbox: List[int]
    value: str
    source: str


class Text(msgspec.Struct):
    word: List[Word]


class VariousFormsOfHangulDataset(msgspec.Struct):
    # info:Info
    image: Image
    # license: License
    text: Text
