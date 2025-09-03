import os
from typing import TypeVar, Type

import msgspec

T = TypeVar("T")


def get_all_image_file_paths(root_dir: str):
    valid_exts = [".jpg", ".jpeg", ".png"]
    file_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if any(f.lower().endswith(ext) for ext in valid_exts):
                full_path = os.path.join(dirpath, f)
                file_paths.append(full_path)
    return file_paths


def get_all_file_paths(root_dir: str, ext: str):
    file_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.lower().endswith(ext.lower()):
                full_path = os.path.join(dirpath, f)
                file_paths.append(full_path)
    return file_paths


def load_label_data(label_path: str, data_model: Type[T]) -> T:
    with open(label_path, "rb") as f:
        json_bytes = f.read()
    data = msgspec.json.decode(json_bytes, type=data_model)
    return data
