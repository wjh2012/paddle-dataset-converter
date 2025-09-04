from typing import List, Tuple, Dict
from app.label_models.various_forms_hangul_data import VariousFormsOfHangulData

from app.rec.rec_data_processor import RecDataProcessor
from app.rec.runner import Runner


class VariousFormsOfHangulProcessor(RecDataProcessor):
    def parse_data(
        self, label_data: VariousFormsOfHangulData
    ) -> Dict[str, List[Tuple[List[List[int]], str]]]:
        # word 모드
        if label_data.text.word:
            results: List[Tuple[List[List[int]], str]] = []
            for idx, word in enumerate(label_data.text.word):
                box = word.wordbox or word.charbox

                if not box or len(box) != 4:
                    raise ValueError(
                        "word 항목의 box는 [x1, y1, x2, y2] 형식이어야 합니다."
                    )
                x1, y1, x2, y2 = map(int, box)
                if x1 >= x2 or y1 >= y2:
                    raise ValueError(f"word[{idx}] box 좌표가 올바르지 않습니다: {box}")

                text = word.value
                if not text:
                    raise ValueError(f"word[{idx}]의 text(value)가 없습니다.")

                quad = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                results.append((quad, text))
            return {"type": "word", "data": results}

        # letter 모드
        elif label_data.text.letter:
            results: List[Tuple[List[List[int]], str]] = []
            letter = label_data.text.letter
            text = letter.value
            results.append(([], text))
            if not text:
                raise ValueError("letter의 text(value)가 없습니다.")
            return {"type": "letter", "data": results}

        else:
            raise ValueError("label_data.text에 word 또는 letter가 없습니다.")


if __name__ == "__main__":
    processor = VariousFormsOfHangulProcessor()
    runner = Runner(
        data_type=VariousFormsOfHangulData,
        data_processor=processor,
    )
    runner.run(
        data_dir=r"D:\ai\ocr_data\다양한 형태의 한글 문자 OCR\Validation\[원천]validation_필기체",
        label_dir=r"D:\ai\ocr_data\다양한 형태의 한글 문자 OCR\Validation\[라벨]validation_필기체",
        save_dir=r"D:\ai\ocr_data\다양한 형태의 한글 문자 OCR\tmp",
    )
