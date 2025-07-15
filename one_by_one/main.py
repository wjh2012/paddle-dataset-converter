from one_by_one.large_handwriting.data_structure import LargeHandwritingData
from one_by_one.large_handwriting.processor import LargeHandwritingDataProcessor
from one_by_one.runner import Runner

fiance_image_path = r"C:\Users\wjh\Downloads\금융업특화OCR\원천데이터"
fiance_label_path = r"C:\Users\wjh\Downloads\금융업특화OCR\라벨링데이터"

kor_pub_doc_image_path = r"C:\Users\wjh\Downloads\공공행정문서\원천데이터"
kor_pub_doc_label_path = r"C:\Users\wjh\Downloads\공공행정문서\라벨링데이터"

fiance_label_image_path = r"C:\Users\wjh\Downloads\OCR데이터(교육)\Sample\01.원천데이터"
fiance_label_label_path = (
    r"C:\Users\wjh\Downloads\OCR데이터(교육)\Sample\02.라벨링데이터"
)

standard_ocr_image_path = r"C:\Users\wjh\Downloads\OCR데이터(교육)\Sample\01.원천데이터"
standard_ocr_label_path = (
    r"C:\Users\wjh\Downloads\OCR데이터(교육)\Sample\02.라벨링데이터"
)

various_forms_of_hangul_image_path = (
    r"C:\Users\wjh\Downloads\다양한형태의한글문자\원천데이터\[원천]Training_인쇄체"
)
various_forms_of_hangul_label_path = (
    r"C:\Users\wjh\Downloads\다양한형태의한글문자\라벨링데이터"
)

large_handwriting_image_path = r"C:\Users\wjh\Downloads\대용량손글씨\원천데이터"
large_handwriting_label_path = r"C:\Users\wjh\Downloads\대용량손글씨\라벨링데이터"

if __name__ == "__main__":
    image_dir = large_handwriting_image_path
    label_dir = large_handwriting_label_path
    save_dir = r"C:\Users\wjh\Desktop\temp_save"

    processor = LargeHandwritingDataProcessor()
    runner = Runner(
        LargeHandwritingData,
        data_processor=processor,
        label_dir=label_dir,
        image_dir=image_dir,
        save_dir=save_dir,
    )

    runner.run()
