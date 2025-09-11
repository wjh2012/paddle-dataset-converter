import os

from app.dict_runner import DictRunner

os.environ["OMP_NUM_THREADS"] = "1"

from app.det_runner import DetRunner
from app.label_data_processor import LabelDataProcessor
from app.rec_runner import RecRunner
from app.utils import get_args

from typing import List, Tuple, Dict
from app.label_models.various_forms_hangul_data import VariousFormsOfHangulData


class VariousFormsOfHangulProcessor(LabelDataProcessor):
    def parse_data(
        self, label_data: VariousFormsOfHangulData
    ) -> Dict[str, List[Tuple[List[List[int]], str]]]:
        # word 모드
        if label_data.text.word:
            results: List[Tuple[List[List[int]], str]] = []

            if label_data.text.type:
                first_box = label_data.text.word[0].charbox
                last_box = label_data.text.word[-1].charbox

                quad = [
                    [first_box[0], min(first_box[1], last_box[1])],
                    [last_box[2], min(first_box[1], last_box[1])],
                    [last_box[2], max(first_box[3], last_box[3])],
                    [first_box[0], max(first_box[3], last_box[3])],
                ]
                text = "".join(word.value for word in label_data.text.word)
                results.append((quad, text))
                return {
                    "type": "word",
                    "imageId": os.path.splitext(label_data.image.file_name)[0],
                    "data": results,
                }

            else:
                for idx, word in enumerate(label_data.text.word):
                    box = word.wordbox or word.charbox

                    if not box or len(box) != 4:
                        raise ValueError(
                            "word 항목의 box는 [x1, y1, x2, y2] 형식이어야 합니다."
                        )
                    x1, y1, x2, y2 = map(int, box)
                    if x1 >= x2 or y1 >= y2:
                        raise ValueError(
                            f"word[{idx}] box 좌표가 올바르지 않습니다: {box}"
                        )

                    text = word.value
                    if not text:
                        raise ValueError(f"word[{idx}]의 text(value)가 없습니다.")

                    quad = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
                    results.append((quad, text))
                return {
                    "type": "word",
                    "imageId": os.path.splitext(label_data.image.file_name)[0],
                    "data": results,
                }

        # letter 모드
        elif label_data.text.letter:
            results: List[Tuple[List[List[int]], str]] = []
            letter = label_data.text.letter
            text = letter.value
            results.append(([], text))
            if not text:
                raise ValueError("letter의 text(value)가 없습니다.")
            return {
                "type": "letter",
                "imageId": os.path.splitext(label_data.image.file_name)[0],
                "data": results,
            }

        else:
            raise ValueError("label_data.text에 word 또는 letter가 없습니다.")


if __name__ == "__main__":
    mode = "rec"
    data_dir = r"D:\ai\ocr_data\various\Validation\[원천]validation_인쇄체"
    label_dir = r"D:\ai\ocr_data\various\Validation\[라벨]validation_인쇄체"
    save_dir = r"D:\ai\ocr_data\various\tmp"
    sampler = 1

    # 1) 인자 파싱 (args가 있을 때만 덮어쓰기)
    try:
        args = get_args()
    except Exception:
        args = None
    if args:
        if getattr(args, "mode", None):
            mode = args.mode
        if getattr(args, "data_dir", None):
            data_dir = args.data_dir
        if getattr(args, "label_dir", None):
            label_dir = args.label_dir
        if getattr(args, "save_dir", None):
            save_dir = args.save_dir
        if getattr(args, "sampler", None):
            sampler = args.sampler

    print("[DEBUG] merged paths:", mode, data_dir, label_dir, save_dir, sampler)

    processor = VariousFormsOfHangulProcessor()

    if mode == "det":
        runner = DetRunner(
            data_type=VariousFormsOfHangulData,
            data_processor=processor,
        )
    elif mode == "rec":
        runner = RecRunner(
            data_type=VariousFormsOfHangulData,
            data_processor=processor,
        )
    elif mode == "dict":
        runner = DictRunner(
            data_type=VariousFormsOfHangulData,
            data_processor=processor,
        )
    else:
        raise ValueError("mode error")

    runner.run(
        data_dir=data_dir, label_dir=label_dir, save_dir=save_dir, sampler=sampler
    )
