from typing import List, Optional

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
    value: str
    source: str
    wordbox: Optional[List[int]] = None
    charbox: Optional[List[int]] = None


class Letter(msgspec.Struct):
    value: str


class Text(msgspec.Struct):
    type: Optional[str] = None
    word: Optional[List[Word]] = None
    letter: Optional[Letter] = None


class VariousFormsOfHangulData(msgspec.Struct):
    # info:Info
    image: Image
    # license: License
    text: Text
