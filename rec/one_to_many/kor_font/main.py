from rec.one_to_many.kor_font.data_structure import filter_annotations
from rec.one_to_many.kor_font.data_loader import read_label_file
from rec.one_to_many.kor_font.txt_maker import make_train_txt


def main():
    json_path = (
        r"D:\ai\ocr_data\13.한국어글자체\02.인쇄체_230721_add\printed_data_info.json"
    )
    image_dir = "images"
    save_txt_path = "train.txt"

    dataset = read_label_file(json_path)
    filtered = filter_annotations(dataset)
    dataset.annotations = filtered
    make_train_txt(dataset, image_dir, save_txt_path)


if __name__ == "__main__":
    main()
