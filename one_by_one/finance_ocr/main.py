import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from one_by_one.finance_ocr.loader import (
    load_label_data,
    get_all_file_paths,
    get_all_image_file_paths,
    load_image_data,
)
from one_by_one.finance_ocr.processor import crop_and_save_words


def main(label_dir: str, image_dir: str, save_dir: str):
    # save_dir/images 디렉토리 경로 생성
    image_save_dir = os.path.join(save_dir, "images")
    txt_save_path = os.path.join(save_dir, "train.txt")

    label_paths = get_all_file_paths(label_dir, ext=".json")
    image_paths = get_all_image_file_paths(image_dir)

    image_file_map = {os.path.basename(p): p for p in image_paths}

    os.makedirs(image_save_dir, exist_ok=True)

    results = []

    max_workers = min(16, os.cpu_count() * 2)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(
                process_single_label, label_path, image_file_map, image_save_dir
            ): label_path
            for label_path in label_paths
        }

        for future in tqdm(as_completed(futures), total=len(futures), desc="진행 중"):
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


def process_single_label(label_path, image_file_map, save_dir):
    label_filename = os.path.basename(label_path)
    image_filename = label_filename.replace(".json", ".jpg")

    if image_filename not in image_file_map:
        print(f"[경고] 이미지 파일 없음: {image_filename}")
        return []

    image_path = image_file_map[image_filename]

    try:
        label_data = load_label_data(label_path)
        image = load_image_data(image_path)
        if image is None:
            print(f"[경고] 이미지 읽기 실패: {image_path}")
            return []

        # crop_and_save_words에서 (crop된 파일명, 단어) 리스트 반환해야 함
        text_entries = crop_and_save_words(label_data, image, image_filename, save_dir)

        return text_entries

    except Exception as e:
        print(f"[에러] 처리 중 예외 발생: {label_path}, 에러: {e}")
        return []


if __name__ == "__main__":
    image_dir = r"C:\Users\wjh\Downloads\금융업특화OCR\원천데이터"
    label_dir = r"C:\Users\wjh\Downloads\금융업특화OCR\라벨링데이터"
    save_dir = r"C:\Users\wjh\Desktop\temp_save"

    main(label_dir=label_dir, image_dir=image_dir, save_dir=save_dir)
