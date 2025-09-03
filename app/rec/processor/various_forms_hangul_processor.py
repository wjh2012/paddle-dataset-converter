import os

import cv2

from app.label_models.various_forms_hangul_data import VariousFormsOfHangulData

from app.rec.rec_data_processor import RecDataProcessor
from app.rec.runner import Runner


class VariousFormsOfHangulProcessor(RecDataProcessor):
    def crop_and_save_words(
        self, label_data: VariousFormsOfHangulData, image, image_filename, save_dir
    ):
        results = []
        base_name = os.path.splitext(os.path.basename(image_filename))[0]

        if label_data.text.word:
            for idx, word_obj in enumerate(label_data.text.word):
                box = word_obj.wordbox or word_obj.charbox
                if not box:
                    print("box 없음")
                    raise
                text = word_obj.value
                if not text:
                    print("text 없음")
                    raise

                x1, y1, x2, y2 = box
                cropped_img = image[y1:y2, x1:x2]

                cropped_filename = f"{base_name}_word_{idx+1}.png"
                save_path = os.path.join(save_dir, cropped_filename)
                cv2.imwrite(save_path, cropped_img)

                # 결과에 추가
                results.append((cropped_filename, text))
        elif label_data.text.letter:
            text = label_data.text.letter.value
            if not text:
                print(f"[경고] letter text 없음: {image_filename}")
                raise

            save_filename = f"{base_name}_letter.png"
            save_path = os.path.join(save_dir, save_filename)
            cv2.imwrite(save_path, image)
            results.append((save_filename, text))

        return results


if __name__ == "__main__":
    processor = VariousFormsOfHangulProcessor()
    runner = Runner(
        data_type=VariousFormsOfHangulData,
        data_processor=processor,
    )
    runner.run(
        data_dir=r"C:\Users\wjh\Downloads\다양한형태의한글문자",
        label_dir=r"C:\Users\wjh\Downloads\다양한형태의한글문자",
        save_dir=r"C:\Users\wjh\Desktop\tmp",
    )
