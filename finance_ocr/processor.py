import os
import cv2
import numpy as np

from finance_ocr.data_structure import FinanceOcrDataset


def crop_and_save_words(label_data: FinanceOcrDataset, image, image_filename, save_dir):
    results = []

    # FinanceOcrDataset의 annotations 안에 polygons가 있음
    for ann in label_data.annotations:
        for idx, polygon in enumerate(ann.polygons):
            text = polygon.text
            points = polygon.points

            if not text:
                continue

            # points는 List[List[int]] 형태, 예: [[x1, y1], [x2, y2], ...]
            x_list = [int(p[0]) for p in points]
            y_list = [int(p[1]) for p in points]

            x_min = max(0, min(x_list))
            x_max = max(0, max(x_list))
            y_min = max(0, min(y_list))
            y_max = max(0, max(y_list))

            # 이미지 크기 내에서 clipping
            h, w = image.shape[:2]
            x_max = min(w, x_max)
            y_max = min(h, y_max)

            cropped_img = image[y_min:y_max, x_min:x_max]

            cropped_filename = f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.jpg"
            save_path = os.path.join(save_dir, cropped_filename)
            cv2.imwrite(save_path, cropped_img)

            results.append((cropped_filename, text))

    return results


def crop_and_save_words_tmp(
    label_data: FinanceOcrDataset, image, image_filename, save_dir
):
    results = []
    h, w = image.shape[:2]

    for ann in label_data.annotations:
        for idx, polygon in enumerate(ann.polygons):
            text = polygon.text
            points = polygon.points

            if not text or not points:
                continue

            # NumPy 배열로 변환
            pts = np.array(points, dtype=np.float32)

            # boundingRect로 axis-aligned 사각형 얻기
            x, y, w_box, h_box = cv2.boundingRect(pts)

            # 이미지 크기 체크
            x_end = min(x + w_box, w)
            y_end = min(y + h_box, h)
            x = max(x, 0)
            y = max(y, 0)

            cropped_img = image[y:y_end, x:x_end]

            cropped_filename = f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.jpg"
            save_path = os.path.join(save_dir, cropped_filename)
            cv2.imwrite(save_path, cropped_img)

            results.append((cropped_filename, text))

    return results
