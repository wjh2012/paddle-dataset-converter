import os


def merge_and_deduplicate_txt_files(directory_path, output_file="result.txt"):
    all_lines = set()

    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)

            # 파일 열고 줄 단위로 읽기
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 개행 문자 제거 후 set에 추가
                for line in lines:
                    all_lines.add(line.rstrip("\n").rstrip("\r"))

    sorted_lines = sorted(all_lines)

    with open(os.path.join(directory_path, output_file), "w", encoding="utf-8") as f:
        for line in sorted_lines:
            f.write(line + "\n")


if __name__ == "__main__":
    merge_and_deduplicate_txt_files("/path/to/your/directory")
