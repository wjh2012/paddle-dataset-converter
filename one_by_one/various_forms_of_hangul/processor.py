import os

import cv2

from one_by_one.various_forms_of_hangul.data_structure import (
    VariousFormsOfHangulDataset,
)


def crop_and_save_words(
    label_data: VariousFormsOfHangulDataset, image, image_filename, save_dir
):
    results = []

    for idx, word_obj in enumerate(label_data.text.word):
        box = word_obj.wordbox
        text = word_obj.value.strip()
        if not text:
            continue

        x1, y1, x2, y2 = box
        cropped_img = image[y1:y2, x1:x2]

        cropped_filename = f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.jpg"
        save_path = os.path.join(save_dir, cropped_filename)
        cv2.imwrite(save_path, cropped_img)

        # 결과에 추가
        results.append((cropped_filename, text))

    return results
