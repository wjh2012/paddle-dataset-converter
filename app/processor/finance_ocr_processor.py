import os
import cv2

from app.label_models.finance_ocr_data import FinanceOcrData
from app.rec.rec_data_processor import RecDataProcessor
from app.rec.runner import Runner


class FinanceOcrProcessor(RecDataProcessor):
    def crop_and_save_words(
        self, label_data: FinanceOcrData, image, image_filename, save_dir
    ):
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

                cropped_filename = (
                    f"{os.path.splitext(image_filename)[0]}_word_{idx+1}.jpg"
                )
                save_path = os.path.join(save_dir, cropped_filename)
                cv2.imwrite(save_path, cropped_img)

                results.append((cropped_filename, text))

        return results


if __name__ == "__main__":
    processor = FinanceOcrProcessor()
    runner = Runner(
        data_type=FinanceOcrData,
        data_processor=processor,
    )
    runner.run(
        data_dir=r"C:\Users\wjh\Downloads\금융업특화OCR",
        label_dir=r"C:\Users\wjh\Downloads\금융업특화OCR",
        save_dir=r"C:\Users\wjh\Desktop",
    )
