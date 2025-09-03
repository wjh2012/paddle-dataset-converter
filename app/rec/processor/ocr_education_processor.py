import os
import cv2

from app.label_models.ocr_education_data import OcrDataEducationData

from app.rec.rec_data_processor import RecDataProcessor


class OcrEducationProcessor(RecDataProcessor):
    def crop_and_save_words(
        self, label_data: OcrDataEducationData, image, image_filename, save_dir
    ):
        results = []

        for idx, bbox_obj in enumerate(label_data.bbox):
            text = bbox_obj.data  # 텍스트
            x_list = bbox_obj.x
            y_list = bbox_obj.y

            if not text:
                continue

            # 사각형 bounding box 계산
            x_min = min(x_list)
            x_max = max(x_list)
            y_min = min(y_list)
            y_max = max(y_list)

            # 좌표 범위 보정 (0 이상)
            x_min = max(0, x_min)
            y_min = max(0, y_min)
            x_max = max(0, x_max)
            y_max = max(0, y_max)

            cropped_img = image[y_min:y_max, x_min:x_max]

            cropped_filename = f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.jpg"
            save_path = os.path.join(save_dir, cropped_filename)
            cv2.imwrite(save_path, cropped_img)

            results.append((cropped_filename, text))

        return results
