from typing import List, Tuple
from app.label_models.various_forms_hangul_data import VariousFormsOfHangulData

from app.rec.rec_data_processor import RecDataProcessor
from app.rec.runner import Runner


class VariousFormsOfHangulProcessor(RecDataProcessor):
    def parse_data(
        self, label_data: VariousFormsOfHangulData
    ) -> List[Tuple[List[List[int]], str]]:

        results: List[Tuple[List[List[int]], str]] = []
        # word 모드
        if getattr(label_data.text, "word", None):
            for idx, word_obj in enumerate(label_data.text.word):
                box = getattr(word_obj, "wordbox", None) or getattr(
                    word_obj, "charbox", None
                )
                if not box or len(box) != 4:
                    raise ValueError(
                        "word 항목의 box는 [x1, y1, x2, y2] 형식이어야 합니다."
                    )
                x1, y1, x2, y2 = map(int, box)
                if x1 >= x2 or y1 >= y2:
                    raise ValueError(f"word[{idx}] box 좌표가 올바르지 않습니다: {box}")

                text = getattr(word_obj, "value", None)
                if not text:
                    raise ValueError(f"word[{idx}]의 text(value)가 없습니다.")

                quad = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                results.append((quad, text))

        # letter 모드
        elif getattr(label_data.text, "letter", None):
            letter = label_data.text.letter
            text = getattr(letter, "value", None)
            if not text:
                raise ValueError("letter의 text(value)가 없습니다.")

            box = getattr(letter, "box", None)
            if not box or len(box) != 4:
                raise ValueError("letter.box는 [x1, y1, x2, y2] 형식이어야 합니다.")
            x1, y1, x2, y2 = map(int, box)
            if x1 >= x2 or y1 >= y2:
                raise ValueError(f"letter box 좌표가 올바르지 않습니다: {box}")

            quad = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
            results.append((quad, text))

        else:
            raise ValueError("label_data.text에 word 또는 letter가 없습니다.")

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
