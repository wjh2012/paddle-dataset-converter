import os
import cv2
import msgspec
import numpy as np
from PIL import Image, ExifTags
from typing import TypeVar, Generic, Type

T = TypeVar("T")


class OcrDataLoader(Generic[T]):
    def __init__(self, data_type: Type[T]):
        self.data_type = data_type

    def get_all_image_file_paths(self, root_dir: str):
        valid_exts = [".jpg", ".jpeg", ".png"]
        file_paths = []
        for dirpath, _, filenames in os.walk(root_dir):
            for f in filenames:
                if any(f.lower().endswith(ext) for ext in valid_exts):
                    full_path = os.path.join(dirpath, f)
                    file_paths.append(full_path)
        return file_paths

    def get_all_file_paths(self, root_dir: str, ext: str):
        file_paths = []
        for dirpath, _, filenames in os.walk(root_dir):
            for f in filenames:
                if f.lower().endswith(ext.lower()):
                    full_path = os.path.join(dirpath, f)
                    file_paths.append(full_path)
        return file_paths

    def load_label_data(self, label_path: str) -> T:
        with open(label_path, "rb") as f:
            json_bytes = f.read()
        data = msgspec.json.decode(json_bytes, type=self.data_type)
        return data

    def load_image_data(self, image_path: str) -> np.ndarray:
        with Image.open(image_path) as pil_image:
            try:
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
                pass

            pil_image = pil_image.convert("RGB")
            image = np.array(pil_image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            return image
