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
                box = word_obj.wordbox or word_obj.charbox
                if not box:
                    print("box 없음")
                    continue
                text = word_obj.value
                if not text:
                    print("text 없음")
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
            if not text:
                print(f"[경고] letter text 없음: {image_filename}")
                return results

            save_filename = f"{os.path.splitext(image_filename)[0]}_letter.png"
            save_path = os.path.join(save_dir, save_filename)
            cv2.imwrite(save_path, image)
            results.append((save_filename, text))

        return results
