import os

import cv2

from one_by_one.kor_pub_doc.data_structure import KorPubDocData
from one_by_one.processor import OcrDataProcessor


class KorPubDocDataProcessor(OcrDataProcessor):
    def crop_and_save_words(
        self, label_data: KorPubDocData, image, image_filename, save_dir
    ):
        results = []

        for idx, annotation in enumerate(label_data.annotations):
            box = annotation.bbox
            text = annotation.text  # ✅ strip 제거 (앞뒤 공백도 유지)

            if not text:
                continue

            # bbox는 [x, y, w, h] 형태
            x, y, w, h = box
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h

            cropped_img = image[y1:y2, x1:x2]

            cropped_filename = f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.jpg"
            save_path = os.path.join(save_dir, cropped_filename)
            cv2.imwrite(save_path, cropped_img)

            results.append((cropped_filename, text))

        return results
