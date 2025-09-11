import os

from app.dict_runner import DictRunner
from app.label_models.finance_ocr_data import FinanceOcrData

os.environ["OMP_NUM_THREADS"] = "1"

from app.det_runner import DetRunner
from app.rec_runner import RecRunner
from app.label_data_processor import LabelDataProcessor
from app.utils import get_args

from typing import List, Tuple, Dict


class FinanceOcrProcessor(LabelDataProcessor):
    def _sort_points(self, points):
        # (x, y) 튜플로 변환
        pts = [tuple(p) for p in points]
        if len(pts) != 4:
            raise ValueError("정확히 4개의 점이 필요합니다.")

        # 1) 전역 x 오름차순 정렬 후 좌/우 그룹으로 분할
        by_x = sorted(pts, key=lambda p: (p[0], p[1]))
        left = by_x[:2]
        right = by_x[2:]

        # 2) 각 그룹에서 y 오름차순으로 정렬 (이미지 좌표계: y가 작을수록 '위')
        tl, bl = sorted(left, key=lambda p: p[1])  # 좌상, 좌하
        tr, br = sorted(right, key=lambda p: p[1])  # 우상, 우하

        return [tl, tr, br, bl]

    def parse_data(
        self, label_data: FinanceOcrData
    ) -> Dict[str, List[Tuple[List[tuple], str]]]:
        # word 모드
        if label_data.annotations:
            results: List[Tuple[List[tuple], str]] = []

            annotation = label_data.annotations[0]
            for idx, polygon in enumerate(annotation.polygons):
                quad = self._sort_points([[int(x), int(y)] for x, y in polygon.points])
                text = polygon.text
                results.append((quad, text))
            return {
                "type": "word",
                "imageId": os.path.splitext(label_data.images[0].name)[0],
                "data": results,
            }

        else:
            raise ValueError("label_data.text에 word 또는 letter가 없습니다.")


if __name__ == "__main__":
    mode = "dict"
    data_dir = r"C:\Users\wjh\Downloads\finance_specialized_ocr\원천데이터"
    label_dir = r"C:\Users\wjh\Downloads\finance_specialized_ocr\라벨링데이터"
    save_dir = r"C:\Users\wjh\Desktop\test"

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

    print("[DEBUG] merged paths:", mode, data_dir, label_dir, save_dir)

    processor = FinanceOcrProcessor()

    if mode == "det":
        runner = DetRunner(
            data_type=FinanceOcrData,
            data_processor=processor,
        )
    elif mode == "rec":
        runner = RecRunner(
            data_type=FinanceOcrData,
            data_processor=processor,
        )
    elif mode == "dict":
        runner = DictRunner(
            data_type=FinanceOcrData,
            data_processor=processor,
        )
    else:
        raise ValueError("mode error")

    runner.run(
        data_dir=data_dir,
        label_dir=label_dir,
        save_dir=save_dir,
    )
