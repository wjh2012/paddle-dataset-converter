from collections import defaultdict
from rec.one_by_one.data_loader import OcrDataLoader, get_all_file_paths
from rec.one_by_one.various_forms_of_hangul.data_structure import (
    VariousFormsOfHangulData,
)


def extract_various_hangul_label_text(label_data: VariousFormsOfHangulData):
    return {
        char
        for word in label_data.text.word
        for char in word.value
        if not char.isspace()
    }


save_dir = "various_char_set.txt"
data_path = (
    "/mnt/data1/ai/dataset/031.다양한_형태의_한글_문자_이미지_인식_데이터/01.데이터"
)

if __name__ == "__main__":
    all_counts = defaultdict(int)

    def process_data(loader, paths, extractor, desc=None):
        for path in paths:
            try:
                data = loader.load_label_data(path)
                chars = extractor(data)
                for char in chars:
                    all_counts[char] += 1
            except Exception as e:
                print(f"[파싱 실패] {path} → {type(e).__name__}: {e}")
                continue

        print(f"{desc} 처리 완료. 현재 총 문자 종류 수: {len(all_counts)}")

    loader = OcrDataLoader(VariousFormsOfHangulData)
    paths = get_all_file_paths(data_path, ext=".json")
    process_data(loader, paths, extract_various_hangul_label_text)

    sorted_chars = sorted(all_counts.keys(), key=lambda x: all_counts[x], reverse=True)

    with open(save_dir, "w", encoding="utf-8") as f:
        for char in sorted_chars:
            f.write(f"{char}\t{all_counts[char]}\n")

    print(f"✅ 문자 빈도를 빈도수 순으로 {save_dir} 파일에 저장 완료!")
