import os
import shutil

import cv2

from rec.one_by_one.processor import OcrDataProcessor
from rec.one_by_one.various_forms_of_hangul.data_structure import (
    VariousFormsOfHangulData,
)


class VariousFormsOfHangulProcessor(OcrDataProcessor):
    def crop_and_save_words(
        self, label_data: VariousFormsOfHangulData, image, image_filename, save_dir
    ):
        results = []

        if label_data.text.word:
            for idx, word_obj in enumerate(label_data.text.word):
                box = word_obj.wordbox
                text = word_obj.value.strip()
                if not text:
                    continue

                x1, y1, x2, y2 = box
                cropped_img = image[y1:y2, x1:x2]

                cropped_filename = (
                    f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.png"
                )
                save_path = os.path.join(save_dir, cropped_filename)
                cv2.imwrite(save_path, cropped_img)

                # 결과에 추가
                results.append((cropped_filename, text))
        elif label_data.text.letter:
            text = label_data.text.letter.value

            # 원본 이미지를 save_dir로 복사
            original_path = os.path.join(self.image_dir, image_filename)
            copied_path = os.path.join(save_dir, image_filename)

            os.makedirs(save_dir, exist_ok=True)
            if not os.path.exists(copied_path):
                shutil.copy(original_path, copied_path)

            # 복사된 파일명을 결과에 추가
            results.append((image_filename, text))

        return results
