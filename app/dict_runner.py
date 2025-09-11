import os
from concurrent.futures import as_completed
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypeVar, Type, List

from tqdm import tqdm

from app.data_loader.label_data_loader import (
    load_label_data,
    get_all_file_paths,
)
from app.label_data_processor import LabelDataProcessor

T = TypeVar("T")


def _process_text(
    label_data_results,
):
    char_set = set()
    for parsed_data in label_data_results:
        for _, text in parsed_data["data"]:
            char_set.update(text)

    sorted_chars = sorted(char_set, key=lambda c: ord(c))
    return sorted_chars


def _process_label(label_path, data_type: Type[T], processor: LabelDataProcessor):
    try:
        label_data = load_label_data(label_path, data_type)
        return processor.parse_data(label_data)
    except Exception as e:
        print(f"[WARN] label parse fail: {label_path} err={e}")
        return None


class DictRunner:
    def __init__(
        self,
        data_type: Type[T],
        data_processor: LabelDataProcessor,
    ):
        self.data_type = data_type
        self.data_processor = data_processor

    def run(self, data_dir, label_dir, save_dir, sampler):

        print("라벨 경로:", label_dir)
        print("저장 경로:", save_dir)

        if label_dir is None:
            print("라벨 경로가 지정되지 않았습니다. (label_dir is None)")
            return

        if save_dir is None:
            print("저장 경로가 지정되지 않았습니다. (save_dir is None)")
            return

        txt_save_path = os.path.join(save_dir, "dict.txt")

        # 3) 입력 파일 목록 수집
        label_paths: List[str] = get_all_file_paths(label_dir, ext=".json")

        if not label_paths:
            print("[오류] 라벨 파일(.json)을 찾지 못했습니다.")
            return

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

        os.makedirs(os.path.dirname(txt_save_path), exist_ok=True)
        processed_char_set = _process_text(label_process_results)
        with open(txt_save_path, "w", encoding="utf-8") as f:
            for char in processed_char_set:
                f.write(f"{char}\n")
