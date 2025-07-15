import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TypeVar, Type

from tqdm import tqdm

from one_by_one.data_loader import OcrDataLoader
from one_by_one.processor import OcrDataProcessor

T = TypeVar("T")


class Runner:
    def __init__(
        self,
        data_type: Type[T],
        data_processor: OcrDataProcessor,
        label_dir,
        image_dir,
        save_dir,
    ):
        self.data_type = data_type
        self.data_loader = OcrDataLoader(self.data_type)
        self.data_processor = data_processor
        self.label_dir = label_dir
        self.image_dir = image_dir
        self.save_dir = save_dir

    def run(self):

        # save_dir/images 디렉토리 경로 생성
        image_save_dir = os.path.join(self.save_dir, "images")
        txt_save_path = os.path.join(self.save_dir, "train.txt")

        label_paths = self.data_loader.get_all_file_paths(self.label_dir, ext=".json")
        image_paths = self.data_loader.get_all_image_file_paths(self.image_dir)

        image_file_map = {
            os.path.splitext(os.path.basename(p))[0]: p for p in image_paths
        }

        os.makedirs(image_save_dir, exist_ok=True)

        results = []

        max_workers = min(16, os.cpu_count() * 2)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    self.process_single_label,
                    label_path,
                    image_file_map,
                    image_save_dir,
                ): label_path
                for label_path in label_paths
            }

            for future in tqdm(
                as_completed(futures), total=len(futures), desc="진행 중"
            ):
                try:
                    text_entries = future.result()
                    if text_entries:
                        results.extend(text_entries)
                except Exception as e:
                    print(f"[에러] Future 예외 발생: {e}")

        # txt 파일 작성
        with open(txt_save_path, "w", encoding="utf-8") as f:
            for image_filename, text in results:
                f.write(f"images/{image_filename}\t{text}\n")

        print(
            f"완료되었습니다.\n크롭 이미지 폴더: {image_save_dir}\n텍스트 파일: {txt_save_path}"
        )

    def process_single_label(self, label_path, image_file_map, image_save_dir):
        label_filename = os.path.basename(label_path)
        basename_without_ext = os.path.splitext(label_filename)[0]

        if basename_without_ext not in image_file_map:
            print(f"[경고] 이미지 파일 없음: {basename_without_ext}")
            return []

        image_path = image_file_map[basename_without_ext]
        image_filename = os.path.basename(image_path)

        try:
            label_data = self.data_loader.load_label_data(label_path)
            image = self.data_loader.load_image_data(image_path)
            if image is None:
                print(f"[경고] 이미지 읽기 실패: {image_path}")
                return []

            # crop_and_save_words에서 (crop된 파일명, 단어) 리스트 반환
            text_entries = self.data_processor.crop_and_save_words(
                label_data, image, image_filename, image_save_dir
            )

            return text_entries

        except Exception as e:
            print(f"[에러] 처리 중 예외 발생: {label_path}, 에러: {e}")
            return []
