import os
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypeVar, Type, Optional, Tuple, List

import cv2
from tqdm import tqdm

from app.data_loader.label_data_loader import (
    get_all_image_file_paths,
    load_label_data,
    get_all_file_paths,
)
from app.data_loader.load_image_data import load_image_data
from app.label_data_processor import LabelDataProcessor

T = TypeVar("T")


def _process_one(
    parsed_data,
    image_path,
    image_save_dir,
) -> Optional[List[Tuple[str, str]]]:
    if not image_path or not os.path.exists(image_path):
        print(f"[WARN] image_path missing for imageId={parsed_data.get('imageId')}")
        return None

    try:
        image = load_image_data(image_path)

        if image is None:
            print(f"[WARN] load_image_data 반환 None: {image_path}")
            return None

        if parsed_data["type"] == "word":
            results: List[Tuple[str, str]] = []

            base_name = os.path.splitext(os.path.basename(image_path))[0]

            for idx, (quad, text) in enumerate(parsed_data["data"]):

                try:
                    x1, y1 = map(int, quad[0])
                    x2, y2 = map(int, quad[2])

                    cropped_img = image[y1:y2, x1:x2]

                    cropped_filename = f"{base_name}_word_{idx+1}.png"
                    save_path = os.path.join(image_save_dir, cropped_filename)
                    cv2.imwrite(save_path, cropped_img)

                    # 결과에 추가
                    results.append((cropped_filename, text))
                except Exception as e:
                    print(
                        f"[WARN] single word crop fail: {image_path} idx={idx} err={e} text={text} quad={quad}"
                    )
                    continue

            return results if results else None

        elif parsed_data["type"] == "letter":
            results: List[Tuple[str, str]] = []

            base_name = os.path.splitext(os.path.basename(image_path))[0]
            quad, text = parsed_data["data"][0]
            save_filename = f"{base_name}_letter.png"
            save_path = os.path.join(image_save_dir, save_filename)
            cv2.imwrite(save_path, image)
            results.append((save_filename, text))
            return results

        else:
            print(f"[WARN] unknown parsed_data type: {parsed_data.get('type')}")
            return None

    except Exception as e:
        print(f"[경고] 처리 실패: image={image_path}, err={e}")
        return None


def _process_label(label_path, data_type: Type[T], processor: LabelDataProcessor):
    try:
        label_data = load_label_data(label_path, data_type)
        return processor.parse_data(label_data)
    except Exception as e:
        print(f"[WARN] label parse fail: {label_path} err={e}")
        return None


class RecRunner:
    def __init__(
        self,
        data_type: Type[T],
        data_processor: LabelDataProcessor,
    ):
        self.data_type = data_type
        self.data_processor = data_processor

    def run(self, data_dir, label_dir, save_dir, sampler):

        print("데이터 경로:", data_dir)
        print("라벨 경로:", label_dir)
        print("저장 경로:", save_dir)
        print("샘플 비율:", sampler)

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

        max_workers = os.cpu_count() or 1

        label_process_results = []
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {
                ex.submit(
                    _process_label, label_path, self.data_type, self.data_processor
                ): label_path
                for label_path in label_paths
            }

            for fut in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="라벨 파싱 진행",
                unit="파일",
            ):
                try:
                    res = fut.result()
                    if res:
                        label_process_results.append(res)
                    else:
                        print(f"[WARN] label future return None")
                except Exception as e:
                    print(f"[WARN] label future exception: {e}")
                    continue

        image_file_map = {
            os.path.splitext(os.path.basename(p))[0]: p for p in image_paths
        }

        valid_label_results = []
        missing_image_ids = []
        for pd in label_process_results:
            if not pd:
                continue
            image_id = pd.get("imageId")
            ipath = image_file_map.get(image_id)
            if ipath:
                valid_label_results.append(pd)
            else:
                missing_image_ids.append(image_id)

        if missing_image_ids:
            print(
                f"[경고] 이미지가 없는 라벨 {len(missing_image_ids)}개 발견. 샘플: {missing_image_ids[:20]}"
            )

        total_valid = len(valid_label_results)
        if total_valid == 0:
            print("[오류] 처리 가능한(이미지 존재) 라벨 항목이 없습니다.")
            return

        valid_label_results = [
            v for idx, v in enumerate(valid_label_results) if idx % sampler == 0
        ]

        image_process_results: List[Tuple[str, str]] = []
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {
                ex.submit(
                    _process_one,
                    parsed_data,
                    image_file_map.get(parsed_data["imageId"]),
                    image_save_dir,
                ): parsed_data
                for parsed_data in valid_label_results
            }

            for fut in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="REC 크롭/저장 진행",
                unit="파일",
            ):
                res = fut.result()
                if not res:
                    print(f"[WARN] crop future return None")
                    continue

                image_process_results.extend(res)

        print(
            f"[정보] 성공적으로 처리된 항목: {len(image_process_results)} / {len(valid_label_results)}"
        )

        # 5) 결과 저장
        if image_process_results:
            with open(txt_save_path, "w", encoding="utf-8") as f:
                for image_filename, text in image_process_results:
                    f.write(f"images/{image_filename}\t{text}\n")

            print(
                f"완료되었습니다.\n크롭 이미지 폴더: {image_save_dir}\n텍스트 파일: {txt_save_path}"
            )
        else:
            print("[경고] 저장할 결과가 없습니다.")
