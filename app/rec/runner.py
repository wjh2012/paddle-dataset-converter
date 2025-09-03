import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import TypeVar, Type, Optional, Tuple, List

from tqdm import tqdm

from app.data_loader.label_data_loader import (
    get_all_image_file_paths,
    load_label_data,
    get_all_file_paths,
)
from app.data_loader.load_image_data import load_image_data
from app.rec.rec_data_processor import RecDataProcessor
from app.rec.utils import get_args

T = TypeVar("T")


def _process_one(
    args: Tuple[str, str, Type[T], str, RecDataProcessor],
) -> Optional[Tuple[str, str]]:
    label_path, image_path, data_type, image_save_dir, processor = args
    try:
        label_data = load_label_data(label_path, data_type)
        image = load_image_data(image_path)
        return processor.crop_and_save_words(
            label_data, image, image_path, image_save_dir
        )
    except Exception as e:
        print(f"[경고] 처리 실패: image={image_path}, label={label_path}, err={e}")
        return None


class Runner:
    def __init__(
        self,
        data_type: Type[T],
        data_processor: RecDataProcessor,
    ):
        self.data_type = data_type
        self.data_processor = data_processor

    def run(
        self,
        data_dir: Optional[str] = None,
        label_dir: Optional[str] = None,
        save_dir: Optional[str] = None,
    ):
        # 1) 인자 파싱 (args가 있을 때만 덮어쓰기)
        try:
            args = get_args()
        except Exception:
            args = None

        if args:
            if data_dir is None:
                data_dir = getattr(args, "data_dir", data_dir)
            if label_dir is None:
                label_dir = getattr(args, "label_dir", label_dir)
            if save_dir is None:
                save_dir = getattr(args, "save_dir", save_dir)

        # 2) 경로 유효성 검사
        print("데이터 경로:", data_dir)
        print("라벨 경로:", label_dir)
        print("저장 경로:", save_dir)

        if label_dir is None:
            print("라벨 경로가 지정되지 않았습니다. (label_dir is None)")
            return
        if data_dir is None:
            print("데이터 경로가 지정되지 않았습니다. (data_dir is None)")
            return
        if save_dir is None:
            print("저장 경로가 지정되지 않았습니다. (save_dir is None)")
            return

        image_save_dir = os.path.join(save_dir, "images")
        txt_save_path = os.path.join(save_dir, "train.txt")
        os.makedirs(image_save_dir, exist_ok=True)

        # 3) 입력 파일 목록 수집
        label_paths: List[str] = get_all_file_paths(label_dir, ext=".json")
        image_paths: List[str] = get_all_image_file_paths(data_dir)

        if not label_paths:
            print("[오류] 라벨 파일(.json)을 찾지 못했습니다.")
            return
        if not image_paths:
            print("[오류] 이미지 파일을 찾지 못했습니다.")
            return

        if len(label_paths) != len(image_paths):
            print(
                f"[경고] 라벨({len(label_paths)})과 이미지({len(image_paths)}) 개수가 다릅니다. "
                f"작은 쪽({min(len(label_paths), len(image_paths))})에 맞춰 진행합니다."
            )

        label_paths.sort()
        image_paths.sort()

        if len(label_paths) != len(image_paths):
            print(
                f"[경고] 라벨({len(label_paths)})과 이미지({len(image_paths)}) 개수가 다릅니다. "
                f"작은 쪽({min(len(label_paths), len(image_paths))})에 맞춰 진행합니다."
            )

        pair_count = min(len(label_paths), len(image_paths))
        label_paths = label_paths[:pair_count]
        image_paths = image_paths[:pair_count]

        # 4) 병렬 실행
        tasks = [
            (lp, ip, self.data_type, image_save_dir, self.data_processor)
            for lp, ip in zip(label_paths, image_paths)
        ]

        results: List[Tuple[str, str]] = []
        max_workers = os.cpu_count() or 1

        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(_process_one, t) for t in tasks]
            for fut in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="크롭/저장 진행",
                unit="파일",
            ):
                res = fut.result()
                if not res:
                    continue
                results.extend(res)

        print(f"[정보] 성공적으로 처리된 항목: {len(results)} / {pair_count}")

        # 5) 결과 저장
        if results:
            with open(txt_save_path, "w", encoding="utf-8") as f:
                for image_filename, text in results:
                    f.write(f"images/{image_filename}\t{text}\n")

            print(
                f"완료되었습니다.\n크롭 이미지 폴더: {image_save_dir}\n텍스트 파일: {txt_save_path}"
            )
        else:
            print("[경고] 저장할 결과가 없습니다.")
