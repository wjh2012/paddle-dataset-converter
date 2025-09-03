import cv2
import numpy as np
from PIL import Image, ExifTags


def load_image_data(image_path: str) -> np.ndarray:
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
