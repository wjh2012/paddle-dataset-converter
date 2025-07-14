import os

import cv2
import msgspec
import numpy as np
from PIL import Image, ExifTags

from finance_ocr.data_structure import FinanceOcrDataset


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


def load_label_data(label_path) -> FinanceOcrDataset:
    with open(label_path, "rb") as f:
        json_bytes = f.read()
    data: FinanceOcrDataset = msgspec.json.decode(json_bytes, type=FinanceOcrDataset)
    return data


def load_image_data(image_path) -> np.ndarray:
    with Image.open(image_path) as pil_image:
        try:
            # Orientation 태그 번호 가져오기
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break

            exif = pil_image._getexif()
            if exif is not None:
                exif_orientation = exif.get(orientation, None)

                if exif_orientation == 3:
                    pil_image = pil_image.rotate(180, expand=True)
                elif exif_orientation == 6:
                    pil_image = pil_image.rotate(-90, expand=True)
                elif exif_orientation == 8:
                    pil_image = pil_image.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # EXIF 정보 없거나 오류 시 무시
            pass

        pil_image = pil_image.convert("RGB")
        image = np.array(pil_image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image
