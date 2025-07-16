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


def extract_ocr_data_public_label_text(label_data: OcrDataPublic):
    return {char for bb in label_data.bbox for char in bb.data if not char.isspace()}


def extract_ocr_data_finance_label_text(label_data: OcrDataFinance):
    return {char for bb in label_data.bbox for char in bb.data if not char.isspace()}


def extract_ocr_data_education_label_text(label_data: OcrDataEducation):
    return {char for bb in label_data.bbox for char in bb.data if not char.isspace()}


def extract_various_hangul_label_text(label_data: VariousFormsOfHangulData):
    return {
        char
        for word in label_data.text.word
        for char in word.value
        if not char.isspace()
    }


def extract_kor_pub_doc_label_text(label_data: KorPubDocData):
    return {
        char
        for ann in label_data.annotations
        for char in ann.text
        if not char.isspace()
    }


def extract_finance_ocr_label_text(label_data: FinanceOcrData):
    return {
        char
        for ann in label_data.annotations
        for polygon in ann.polygons
        for char in polygon.text
        if not char.isspace()
    }


def extract_large_handwriting_label_text(label_data: LargeHandwritingData):
    return {char for b in label_data.bbox for char in b.data if not char.isspace()}


if __name__ == "__main__":
    all_results = set()

    # 1️⃣ Standard OCR
    # 공공
    standard_loader = OcrDataLoader(OcrDataPublic)
    ocr_data_public_paths = get_all_file_paths(ocr_data_public_label_dir, ext=".json")
    ocr_data_public_char = set()
    for path in ocr_data_public_paths:
        data = standard_loader.load_label_data(path)
        chars = extract_ocr_data_public_label_text(data)
        ocr_data_public_char.update(chars)
    print("OCR 데이터(공공) 문자:", ocr_data_public_char)
    all_results.update(ocr_data_public_char)

    # 교육
    standard_loader = OcrDataLoader(OcrDataEducation)
    ocr_data_education_paths = get_all_file_paths(
        ocr_data_education_label_dir, ext=".json"
    )
    ocr_data_education_char = set()
    for path in ocr_data_education_paths:
        data = standard_loader.load_label_data(path)
        chars = extract_ocr_data_education_label_text(data)
        ocr_data_education_char.update(chars)
    print("OCR 데이터(교육) 문자:", ocr_data_education_char)
    all_results.update(ocr_data_education_char)

    # 금융
    standard_loader = OcrDataLoader(OcrDataFinance)
    ocr_data_finance_paths = get_all_file_paths(ocr_data_finance_label_dir, ext=".json")
    ocr_data_finance_char = set()
    for path in ocr_data_finance_paths:
        data = standard_loader.load_label_data(path)
        chars = extract_ocr_data_finance_label_text(data)
        ocr_data_finance_char.update(chars)
    print("OCR 데이터(금융) 문자:", ocr_data_finance_char)
    all_results.update(ocr_data_finance_char)

    # 2️⃣ Various Forms of Hangul
    hangul_paths = get_all_file_paths(various_forms_hangul_label_dir, ext=".json")
    hangul_loader = OcrDataLoader(VariousFormsOfHangulData)
    hangul_chars = set()
    for path in hangul_paths:
        data = hangul_loader.load_label_data(path)
        chars = extract_various_hangul_label_text(data)
        hangul_chars.update(chars)
    print("Various Forms of Hangul 문자:", hangul_chars)
    all_results.update(hangul_chars)

    # 3️⃣ Korean Public Document
    kor_pub_paths = get_all_file_paths(kor_pub_doc_label_dir, ext=".json")
    kor_pub_loader = OcrDataLoader(KorPubDocData)
    kor_pub_chars = set()
    for path in kor_pub_paths:
        data = kor_pub_loader.load_label_data(path)
        chars = extract_kor_pub_doc_label_text(data)
        kor_pub_chars.update(chars)
    print("Korean Public Document 문자:", kor_pub_chars)
    all_results.update(kor_pub_chars)

    # 4️⃣ Finance OCR
    finance_paths = get_all_file_paths(finance_ocr_label_dir, ext=".json")
    finance_loader = OcrDataLoader(FinanceOcrData)
    finance_chars = set()
    for path in finance_paths:
        data = finance_loader.load_label_data(path)
        chars = extract_finance_ocr_label_text(data)
        finance_chars.update(chars)
    print("Finance OCR 문자:", finance_chars)
    all_results.update(finance_chars)

    # 5️⃣ Large Handwriting
    large_paths = get_all_file_paths(large_handwriting_label_dir, ext=".json")
    large_loader = OcrDataLoader(LargeHandwritingData)
    large_chars = set()
    for path in large_paths:
        data = large_loader.load_label_data(path)
        chars = extract_large_handwriting_label_text(data)
        large_chars.update(chars)
    print("Large Handwriting 문자:", large_chars)
    all_results.update(large_chars)

    # ✅ 모든 데이터셋 합친 문자 집합 출력
    print("모든 데이터셋에서 수집된 전체 문자:", all_results)

    # ✅ 파일로 저장 (한 줄에 한 문자)
    with open("all_results.txt", "w", encoding="utf-8") as f:
        for char in sorted(all_results):
            f.write(char + "\n")

    print("✅ 모든 문자 집합을 all_results.txt 파일에 저장 완료!")
