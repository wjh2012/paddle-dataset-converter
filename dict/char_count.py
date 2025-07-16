from collections import defaultdict
from one_by_one.data_loader import OcrDataLoader, get_all_file_paths
from one_by_one.finance_ocr.data_structure import FinanceOcrData
from one_by_one.kor_pub_doc.data_structure import KorPubDocData
from one_by_one.large_handwriting.data_structure import LargeHandwritingData
from one_by_one.ocr_data_education.data_structure import OcrDataEducation
from one_by_one.ocr_data_finance.data_structure import OcrDataFinance
from one_by_one.ocr_data_public.data_structure import OcrDataPublic
from one_by_one.various_forms_of_hangul.data_structure import VariousFormsOfHangulData

ocr_data_public_label_dir = (
    r"C:\Users\wjh\Downloads\OCR데이터(공공)\Sample\02.라벨링데이터"
)
ocr_data_education_label_dir = (
    r"C:\Users\wjh\Downloads\OCR데이터(교육)\Sample\02.라벨링데이터"
)
ocr_data_finance_label_dir = (
    r"C:\Users\wjh\Downloads\OCR데이터(금융및물류)\Sample\02.라벨링데이터"
)

various_forms_hangul_label_dir = (
    r"C:\Users\wjh\Downloads\다양한형태의한글문자\라벨링데이터"
)
kor_pub_doc_label_dir = r"C:\Users\wjh\Downloads\공공행정문서\라벨링데이터"
finance_ocr_label_dir = r"C:\Users\wjh\Downloads\금융업특화OCR\라벨링데이터"
large_handwriting_label_dir = r"C:\Users\wjh\Downloads\대용량손글씨\라벨링데이터"


def extract_chars_from_bboxes(bboxes):
    chars = []
    for bb in bboxes:
        chars.extend([c for c in bb.data if not c.isspace()])
    return chars


def extract_ocr_data_public_label_text(label_data: OcrDataPublic):
    return extract_chars_from_bboxes(label_data.bbox)


def extract_ocr_data_finance_label_text(label_data: OcrDataFinance):
    return extract_chars_from_bboxes(label_data.bbox)


def extract_ocr_data_education_label_text(label_data: OcrDataEducation):
    return extract_chars_from_bboxes(label_data.bbox)


def extract_various_hangul_label_text(label_data: VariousFormsOfHangulData):
    chars = []
    for word in label_data.text.word:
        chars.extend([c for c in word.value if not c.isspace()])
    return chars


def extract_kor_pub_doc_label_text(label_data: KorPubDocData):
    chars = []
    for ann in label_data.annotations:
        chars.extend([c for c in ann.text if not c.isspace()])
    return chars


def extract_finance_ocr_label_text(label_data: FinanceOcrData):
    chars = []
    for ann in label_data.annotations:
        for polygon in ann.polygons:
            chars.extend([c for c in polygon.text if not c.isspace()])
    return chars


def extract_large_handwriting_label_text(label_data: LargeHandwritingData):
    return extract_chars_from_bboxes(label_data.bbox)


if __name__ == "__main__":
    all_counts = defaultdict(int)

    def process_data(loader, paths, extractor, desc):
        for path in paths:
            data = loader.load_label_data(path)
            chars = extractor(data)
            for char in chars:
                all_counts[char] += 1
        print(f"{desc} 처리 완료. 현재 총 문자 종류 수: {len(all_counts)}")

    # 공공
    loader = OcrDataLoader(OcrDataPublic)
    paths = get_all_file_paths(ocr_data_public_label_dir, ext=".json")
    process_data(loader, paths, extract_ocr_data_public_label_text, "OCR 데이터(공공)")

    # 교육
    loader = OcrDataLoader(OcrDataEducation)
    paths = get_all_file_paths(ocr_data_education_label_dir, ext=".json")
    process_data(
        loader, paths, extract_ocr_data_education_label_text, "OCR 데이터(교육)"
    )

    # 금융
    loader = OcrDataLoader(OcrDataFinance)
    paths = get_all_file_paths(ocr_data_finance_label_dir, ext=".json")
    process_data(loader, paths, extract_ocr_data_finance_label_text, "OCR 데이터(금융)")

    # 다양한 형태의 한글
    loader = OcrDataLoader(VariousFormsOfHangulData)
    paths = get_all_file_paths(various_forms_hangul_label_dir, ext=".json")
    process_data(
        loader, paths, extract_various_hangul_label_text, "Various Forms of Hangul"
    )

    # 공공행정문서
    loader = OcrDataLoader(KorPubDocData)
    paths = get_all_file_paths(kor_pub_doc_label_dir, ext=".json")
    process_data(
        loader, paths, extract_kor_pub_doc_label_text, "Korean Public Document"
    )

    # 금융 특화 OCR
    loader = OcrDataLoader(FinanceOcrData)
    paths = get_all_file_paths(finance_ocr_label_dir, ext=".json")
    process_data(loader, paths, extract_finance_ocr_label_text, "Finance OCR")

    # 대용량 손글씨
    loader = OcrDataLoader(LargeHandwritingData)
    paths = get_all_file_paths(large_handwriting_label_dir, ext=".json")
    process_data(
        loader, paths, extract_large_handwriting_label_text, "Large Handwriting"
    )

    # ✅ 파일로 저장 (빈도수 순 정렬)
    sorted_chars = sorted(all_counts.keys(), key=lambda x: all_counts[x], reverse=True)

    with open("all_results_with_count_sorted.txt", "w", encoding="utf-8") as f:
        for char in sorted_chars:
            f.write(f"{char}\t{all_counts[char]}\n")

    print(
        "✅ 문자 빈도를 빈도수 순으로 all_results_with_count_sorted.txt 파일에 저장 완료!"
    )
