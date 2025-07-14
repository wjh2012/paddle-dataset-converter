import os

from kor_font.data_structure import KorFontDataset


def make_train_txt(dataset: KorFontDataset, image_dir: str, save_txt_path: str):
    # image_id → file_name dict 생성
    image_map = {img.id: img.file_name for img in dataset.images}

    lines = []

    for ann in dataset.annotations:
        file_name = image_map.get(ann.image_id)
        if not file_name:
            print(f"⚠️ Warning: image_id '{ann.image_id}' not found in images list")
            continue

        # 이미지 경로: images/파일명
        image_path = os.path.join(image_dir, file_name).replace(
            "\\", "/"
        )  # Windows 호환
        text = ann.text

        line = f"{image_path}\t{text}"
        lines.append(line)

    # 파일 저장
    with open(save_txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ Saved train.txt to: {save_txt_path}")
