import os

import cv2
import msgspec
import numpy as np
from PIL import Image

from various_forms_of_hangul.data_structure import VariousFormsOfHangulDataset


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


def load_label_data(label_path) -> VariousFormsOfHangulDataset:
    with open(label_path, "rb") as f:
        json_bytes = f.read()
    data: VariousFormsOfHangulDataset = msgspec.json.decode(
        json_bytes, type=VariousFormsOfHangulDataset
    )
    return data


def load_image_data(image_path) -> np.ndarray:
    with Image.open(image_path) as pil_image:
        pil_image = pil_image.convert("RGB")
        image = np.array(pil_image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image
