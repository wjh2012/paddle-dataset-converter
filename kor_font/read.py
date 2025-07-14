import msgspec

from kor_font.data_structure import KorFontDataset


def read(label_dir, image_dir):
    read_label_file(label_dir)
    read_image_dir(image_dir)


def read_label_file(label_file_path: str):
    with open(label_file_path, "rb") as f:
        json_bytes = f.read()
    data: KorFontDataset = msgspec.json.decode(json_bytes, type=KorFontDataset)
    return data


def read_image_dir(image_dir):
    pass


if __name__ == "__main__":
    json_path = r"C:\Users\wjh\Downloads\한국어글자체\라벨링데이터\handwriting_data_info_clean.json"
    dataset = read_label_file(json_path)
